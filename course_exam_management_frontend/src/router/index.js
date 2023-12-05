import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from "@/store";


function checkUserStudentPermission(to) {
    console.log(to.path)
    if (store.getters.fetchMe.is_student && to.path === '/') {
        return true
    }

    return false

}

const routes = [
    {
        path: '/login',
        name: 'login',
        meta: {
            requiresAuth: false
        },
        component: () => import('../views/auth/Login.vue'),
    },
    {
        path: '/signup',
        name: 'signup',
        meta: {
            requiresAuth: false
        },
        component: () => import('../views/auth/SignUp.vue'),
    },
    {
        path: '/forget-password',
        name: 'forget-password',
        meta: {
            requiresAuth: false
        },
        component: () => import('../views/auth/ForgotPassword.vue'),
    },
    {
        path: '/',
        name: 'home',
        component: HomeView,
        meta: {
            requiresAuth: true
        },
        children: [
            {
                path: "/chat",
                component: () => import("../views/ChatLayout.vue"),
                name: "ChatLayout",
                children: [
                {
                path: "",
                component: () => import("../views/Chat.vue"),
                name: "Chat",
                },
                ],
            },
            {
                path: "",
                component: () => import('../views/Course.vue'),
                name: "courses",
                children: []

            },
            {
                path: "/classes",
                component: () => import('../views/Classes.vue'),
                name: "classes",
            },
            {
                path: "/quiz",
                component: () => import('../views/Quiz.vue'),
                name: "quiz",
            },
            {
                path: "/start_quiz/:id/",
                component: () => import('../components/QuizView.vue'),
                name: "start_quiz",
                props: true
            },
            {
                path: "/change-password",
                component: () => import('../views/auth/ChangePassword.vue'),
                name: "change_password",
            },
            {
                path: "/course_detail/:id/",
                component: () => import('../components/CourseDetail.vue'),
                name: "courses_detail",
            },
            {
                path: "/student_course_detail/:id/",
                component: () => import('../components/StudentCourseDetail.vue'),
                name: "student_courses_detail",
            },
            {
                path: "/grades",
                component: () => import('../components/CourseList.vue'),
                name: "grade",

            },
            {
                path: "/student_detail/:id/",
                component: () => import('../components/StudentDetail.vue'),
                name: "student_detail",
            },
            {
                path: "/courses_students/:id/",
                component: () => import('../components/CourseStudentsList.vue'),
                name: "course_student_list",
                children: [
                    {
                        path: ":student_id/",
                        component: () => import('../components/StudentDetail.vue'),
                        name: "student_grades",
                    },
                ]

            },
            {
                path: "/users",
                component: () => import('../views/User.vue'),
                name: "users",
                // beforeEnter: (to, from, next) => {
                //     // reject the navigation
                //     if (store.getters.fetchMe.is_superuser) {
                //         return true
                //     } else {
                //         return next('/')
                //     }
                // },
            },
        ]

    },

]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    base: process.env.VUE_APP_BASE_URL,
    routes
})

router.beforeEach(async (to, from, next) => {

    // console.log(to.meta)
    const token = localStorage.getItem('auth-token')
    // console.log(!to.meta.requiresAuth)
    if (to.meta.requiresAuth === false) {
        return next()
    }

    if (to.meta.requiresAuth && token === null) {
        return next('/login')
    }
    console.log(!store.getters.fetchMe)
    if (!store.getters.fetchMe) {
        await store.dispatch('getMe');
    }

    return next()

})

export default router
