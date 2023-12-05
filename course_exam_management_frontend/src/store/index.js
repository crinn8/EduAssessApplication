import {createStore} from 'vuex'
import {api} from "@/utils/axios";
import createPersistedState from 'vuex-persistedstate';
import router from "@/router";

export default createStore({
    state: {
        me: {},
        pythonQuizSolution: []
    },
    getters: {
        fetchMe(state) {
            return state.me
        },
        getPythonQuizSolution(state) {
            return state.pythonQuizSolution
        }
    },
    mutations: {
        setMe(state, response) {
            state.me = response.data
        },
        setPythonQuizSolution(state, response) {
            state.pythonQuizSolution = response
        }
    },
    actions: {
        async getMe({commit}) {
            await api.get('/auth/users/me/').then(response => {
                commit("setMe", response)
                router.push('/')
            })
        },
        // addPythonQuizSolution({commit}) {
        //
        // }
    },
    plugins: [createPersistedState({
        paths: ['me'], // Only persist the 'me' state
        storage: window.localStorage // Use localStorage for persistence
    })],
    modules: {}
})
