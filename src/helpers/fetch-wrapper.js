import axios from "axios";
import { useAuthStore } from "@/stores/auth.store.js";
import baseUrl from "@/helpers/base.js";

export const fetchWrapper = {
  get: request("GET"),
  post: request("POST"),
  put: request("PUT"),
  delete: request("DELETE"),
};

function request(method) {
  return async (url, body = null) => {
    try {
      const config = {
        method,
        url: url.startsWith(baseUrl) ? url : `${baseUrl}${url}`,
        headers: authHeader(url),
        data: body,
      };

      const response = await axios(config);
      return response.data; // Axios автоматически парсит JSON
    } catch (error) {
      return handleResponse(error);
    }
  };
}

// 🔹 Формируем заголовки авторизации
function authHeader(url) {
  const { accessToken } = useAuthStore();
  const isLoggedIn = !!accessToken;
  const isApiUrl = url.startsWith(baseUrl);

  if (isLoggedIn && isApiUrl) {
    return { Authorization: `BMDU ${accessToken}` };
  }
  return {};
}

// 🔹 Обработка ошибок
async function handleResponse(error) {
  const { accessToken, refreshToken, logout, setTokens } = useAuthStore();

  if (error.response) {
    // Если 401 Unauthorized
    if (error.response.status === 401 && accessToken && refreshToken) {
      try {
        // Попытаться обновить токен
        const refreshed = await refreshAccessToken(refreshToken);
        if (refreshed) {
          // Повторяем запрос с обновленным токеном
          const retryConfig = error.config;
          retryConfig.headers["Authorization"] = `BMDU ${useAuthStore().accessToken}`;
          const retryResponse = await axios(retryConfig);
          return retryResponse.data; // Возвращаем данные с повторного запроса
        }
      } catch (refreshError) {
        console.log("Ошибка обновления токена:", refreshError);
      }
    }

    // Если ошибка 401 или 403 и accessToken есть, разлогиниваем
    if ([401, 403].includes(error.response.status) && accessToken) {
      console.log("Ошибка авторизации, разлогиниваем пользователя");
      logout();
    }

    return Promise.reject(error.response.data?.message || error.response.statusText);
  }

  return Promise.reject("Network error");
}

// 🔹 Функция обновления токена
async function refreshAccessToken(refreshToken) {
  const { setTokens } = useAuthStore();
  try {
    const response = await axios.post(`${baseUrl}/api/token/refresh/`, { refresh: refreshToken });
    setTokens(response.data.access, refreshToken);
    return true;
  } catch (error) {
    return false; // Ошибка при обновлении токена
  }
}
