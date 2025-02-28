import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import guards from "@/router/guards.js";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login-page",
      component: () => import("../views/LoginView.vue"),
      meta: {
        layout: "EmptyLayout",
        title: "Giriş",
        adminRequired: false,
      },
      beforeEnter: guards.defaultGuard,
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        layout: "MainLayout",
        title: "Baş sahypa",
        adminRequired: false,
      },
      beforeEnter: guards.authGuard,
    },
    {
      path: "/high-schools",
      name: "high-schools",
      component: () => import("../views/HighSchoolViews/HighSchools.vue"),
      meta: {
        layout: "MainLayout",
        title: "Ýokary okuw mekdepleri",
        adminRequired: true,
      },
      children: [
        {
          path: "",
          name: "high-schools-list",
          component: () =>
            import("../views/HighSchoolViews/HighSchoolsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýokary okuw mekdepleri",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "add",
          name: "add-high-school",
          component: () =>
            import("../views/HighSchoolViews/AddHighSchoolView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýokary okuw mekdebi goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-high-school",
          component: () =>
            import("../views/HighSchoolViews/EditHighSchoolView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýokary okuw mekdebi üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "view/:id",
          name: "about-high-school",
          component: () =>
            import("../views/HighSchoolViews/AboutHighSchool.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýokary okuw mekdebi",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
          children: [
            {
              path: "",
              name: "high-school",
              component: () =>
                import("../views/HighSchoolViews/ViewHighSchoolView.vue"),
              beforeEnter: guards.authGuard,
              meta: {
                layout: "MainLayout",
                title: "Ýokary okuw mekdebi",
                adminRequired: true,
              },
            },
            {
              path: "faculties",
              name: "high-school-faculties",
              component: () =>
                import("../views/HighSchoolViews/HighSchoolFacultiesView.vue"),
              beforeEnter: guards.authGuard,
              meta: {
                layout: "MainLayout",
                title: "Ýokary okuw mekdebiň fakultetleri",
                adminRequired: true,
              },
            },
            {
              path: "specializations",
              name: "high-school-specializations",
              component: () =>
                import(
                  "../views/HighSchoolViews/HighSchoolSpecializationsView.vue"
                ),
              beforeEnter: guards.authGuard,
              meta: {
                layout: "MainLayout",
                title: "Ýokary okuw mekdebiň hünarleri",
                adminRequired: true,
              },
            },
            {
              path: "departments",
              name: "high-school-departments",
              component: () =>
                import(
                  "../views/HighSchoolViews/HighSchoolDepartmentsView.vue"
                ),
              beforeEnter: guards.authGuard,
              meta: {
                layout: "MainLayout",
                title: "Ýokary okuw mekdebiň kafedralary",
                adminRequired: true,
              },
            },
          ],
        },
      ],
      beforeEnter: guards.authGuard,
    },
    {
      path: "/faculties",
      name: "faculties",
      component: () => import("../views/FacultyViews/Faculties.vue"),
      meta: {
        layout: "MainLayout",
        title: "Fakultetler",
      },
      children: [
        {
          path: "",
          name: "faculties-list",
          component: () =>
            import("../views/FacultyViews/FacultiesListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Fakultetler",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-faculty",
          component: () => import("../views/FacultyViews/AddFacultyView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Fakultet goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-faculty",
          component: () => import("../views/FacultyViews/EditFacultyView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Fakulteti üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/departments",
      name: "departments",
      component: () => import("../views/DepartmentViews/Departments.vue"),
      meta: {
        layout: "MainLayout",
        title: "Kafedralar",
      },
      children: [
        {
          path: "",
          name: "departments-list",
          component: () =>
            import("../views/DepartmentViews/DepartmentsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Kafedralar",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-department",
          component: () =>
            import("../views/DepartmentViews/AddDepartmentView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Kafedra goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-department",
          component: () =>
            import("../views/DepartmentViews/EditDepartmentView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Kafedrany üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/specializations",
      name: "specializations",
      component: () =>
        import("../views/SpecializationViews/Specializations.vue"),
      meta: {
        layout: "MainLayout",
        title: "Hünärler",
      },
      children: [
        {
          path: "",
          name: "specializations-list",
          component: () =>
            import("../views/SpecializationViews/SpecializationsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Hünarler",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-specialization",
          component: () =>
            import("../views/SpecializationViews/AddSpecializationView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Hünär goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-specialization",
          component: () =>
            import("../views/SpecializationViews/EditSpecializationView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Hünäri üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/nationalizations",
      name: "nationalizations",
      component: () =>
        import("../views/NationalizationViews/Nationalizations.vue"),
      meta: {
        layout: "MainLayout",
        title: "Milletler",
      },
      children: [
        {
          path: "",
          name: "nationalizations-list",
          component: () =>
            import(
              "../views/NationalizationViews/NationalizationsListView.vue"
            ),
          meta: {
            layout: "MainLayout",
            title: "Milletler",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-nationalization",
          component: () =>
            import("../views/NationalizationViews/AddNationalizationView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Millet goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-nationalization",
          component: () =>
            import("../views/NationalizationViews/EditNationalizationView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Milleti üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/countries",
      name: "countries",
      component: () => import("../views/CountryViews/Countries.vue"),
      meta: {
        layout: "MainLayout",
        title: "Ýurtlar",
      },
      children: [
        {
          path: "",
          name: "countries-list",
          component: () =>
            import("../views/CountryViews/CountriesListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýurtlar",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-country",
          component: () => import("../views/CountryViews/AddCountryView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýurt goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-country",
          component: () => import("../views/CountryViews/EditCountryView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Ýurdy üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/regions",
      name: "regions",
      component: () => import("../views/RegionViews/Regions.vue"),
      meta: {
        layout: "MainLayout",
        title: "Welaýatlar",
      },
      children: [
        {
          path: "",
          name: "regions-list",
          component: () => import("../views/RegionViews/RegionsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Welaýatlar",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-region",
          component: () => import("../views/RegionViews/AddRegionView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Welaýat goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-region",
          component: () => import("../views/RegionViews/EditRegionView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Welaýaty üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/classificators",
      name: "classificators",
      component: () => import("../views/ClassificatorViews/Classificators.vue"),
      meta: {
        layout: "MainLayout",
        title: "Klassifikatorlar",
        adminRequired: true,
      },
      beforeEnter: guards.authGuard,
      children: [
        {
          path: "",
          name: "classificators-list",
          component: () =>
            import("../views/ClassificatorViews/ClassificatorsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Klassifikatorlar",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "add",
          name: "add-classificator",
          component: () =>
            import("../views/ClassificatorViews/AddClassificatorView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Klassifikator goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-classificator",
          component: () =>
            import("../views/ClassificatorViews/EditClassificatorView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Klassifikatory üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/degrees",
      name: "degrees",
      component: () => import("../views/DegreeViews/Degrees.vue"),
      meta: {
        layout: "MainLayout",
        title: "Hünär derejeleri",
        adminRequired: true,
      },
      beforeEnter: guards.authGuard,
      children: [
        {
          path: "",
          name: "degrees-list",
          component: () => import("../views/DegreeViews/DegreesListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Hünär derejeleri",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "add",
          name: "add-degree",
          component: () => import("../views/DegreeViews/AddDegreeView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Hünär derejesi goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-degree",
          component: () => import("../views/DegreeViews/EditDegreeView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Hünär derejesini üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/students",
      name: "students",
      component: () => import("../views/StudentViews/Students.vue"),
      meta: {
        layout: "MainLayout",
        title: "Talyplar",
      },
      beforeEnter: guards.defaultGuard,
      children: [
        {
          path: "",
          name: "students-list",
          component: () => import("../views/StudentViews/StudentsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Talyplar",
          },
          beforeEnter: guards.defaultGuard,
        },
        {
          path: "add",
          name: "add-student",
          component: () => import("../views/StudentViews/AddStudentView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Talyp goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        // FIXME
        {
          path: "edit/:id",
          name: "edit-student",
          component: () => import("../views/StudentViews/EditStudentView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Talyp maglumatyny üýtgetmek",
            staffRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "view/:id",
          name: "view-student",
          component: () => import("../views/StudentViews/StudentInfoView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Talyp barada maglumat",
          },
          beforeEnter: guards.defaultGuard,
        },
      ],
    },
    {
      path: "/expulsion-reasons",
      name: "expulsion-reasons",
      component: () =>
        import("../views/ExpulsionReasonViews/ExpulsionReasons.vue"),
      meta: {
        layout: "MainLayout",
        title: "Okuwdan çykarma sebäpleri",
      },
      children: [
        {
          path: "",
          name: "expulsion-reasons-list",
          component: () =>
            import(
              "../views/ExpulsionReasonViews/ExpulsionReasonsListView.vue"
            ),
          meta: {
            layout: "MainLayout",
            title: "Okuwdan çykarma sebäpleri",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "add",
          name: "add-expulsion-reason",
          component: () =>
            import("../views/ExpulsionReasonViews/AddExpulsionReasonView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Okuwdan çykarma sebäbini goşmak",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "edit/:id",
          name: "edit-expulsion-reason",
          component: () =>
            import("../views/ExpulsionReasonViews/EditExpulsionReasonView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Okuwdan çykarma sebäbini üýtgetmek",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/expelled-students",
      name: "expelled-students",
      component: () =>
        import("../views/ExpelledStudentViews/ExpelledStudents.vue"),
      meta: {
        layout: "MainLayout",
        title: "Okuwdan boşadylanlar",
        staffRequired: true,
      },
      children: [
        {
          path: "",
          name: "expelled-students-list",
          component: () =>
            import(
              "../views/ExpelledStudentViews/ExpelledStudentsListView.vue"
            ),
          meta: {
            layout: "MainLayout",
            title: "Okuwdan boşadylanlar",
            staffRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: "reinstate/:id",
          name: "reinstate-student",
          component: () =>
            import(
              "../views/ExpelledStudentViews/ReinstateExpelledStudentView.vue"
            ),
          meta: {
            layout: "MainLayout",
            title: "Dikeltmek",
            staffRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/statements",
      name: "statements",
      component: () => import("../views/StatementViews/Statements.vue"),
      meta: {
        layout: "MainLayout",
        title: "Arzalar",
      },
      children: [
        {
          path: "",
          name: "statements-list",
          component: () =>
            import("../views/StatementViews/StatementsListView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Arzalar",
            adminRequired: true,
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: ":id/expulsion",
          name: "verdict-expulsion-statement",
          component: () =>
            import("../views/StatementViews/VerdictStatementView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Okuwdan boşatmak arzasy",
            adminRequired: true,
            statementType: "expulsion",
          },
          beforeEnter: guards.authGuard,
        },
        {
          path: ":id/reinstate",
          name: "verdict-reinstate-statement",
          component: () =>
            import("../views/StatementViews/VerdictStatementView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Okuwy dikeltmek arzasy",
            adminRequired: true,
            statementType: "reinstate",
          },
          beforeEnter: guards.authGuard,
        },
      ],
    },
    {
      path: "/diplomas",
      name: "diplomas",
      component: () => import("../views/DiplomasViews/Diplomas.vue"),
      meta: {
        layout: "MainLayout",
        title: "Diplomalar",
      },
      children: [
        {
          path: "",
          name: "diplomas-view",
          component: () => import("../views/DiplomasViews/DiplomasView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Diplomlar",
          },
        },
        {
          path: "add",
          name: "add-diploma-request",
          component: () =>
            import("../views/DiplomasViews/AddDiplomaRequest.vue"),
          meta: {
            layout: "MainLayout",
            title: "Diplom hasabatyny döretmek",
            stuffRequired: true,
          },
        },
        {
          path: "new-request",
          name: "new-diploma-request",
          component: () => import("../views/DiplomasViews/NewRequestView.vue"),
          meta: {
            layout: "MainLayout",
            title: "Diplom hasabatyny täzelemek",
            stuffRequired: true,
          },
        },
      ],
    },
    {
      path: "/secondary-schools",
      name: "secondary-schools",
      component: () => import("../views/SecondarySchoolsView.vue"),
      meta: {
        layout: "MainLayout",
        title: "Orta hünär mekdepleri",
        adminRequired: true,
      },
      beforeEnter: guards.authGuard,
    },
    {
      path: "/403",
      name: "page-403",
      component: () => import("@/views/Errors/Page403.vue"),
      meta: {
        layout: "EmptyLayout",
        title: "403 | Rugsat ýok",
        adminRequired: false,
      },
      beforeEnter: guards.defaultGuard,
    },
    {
      path: "/:pathMatch(.*)*",
      component: () => import("../views/Errors/Page404.vue"),
    },
  ],
});

export default router;
