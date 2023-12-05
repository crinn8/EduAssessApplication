import axios from "axios";
import router from "@/router";

console.log(process.env.VUE_APP_BASE_URL)
export const api = axios.create({
    baseURL: process.env.VUE_APP_BASE_URL
});


api.interceptors.request.use(
    function (config) {
        localStorage.getItem('auth-token') ? config.headers.Authorization = `Token ${localStorage.getItem('auth-token')}` : ''
        return config;
    },
    function (error) {
        // Do something with request error
        return Promise.reject(error);
    }
);


api.interceptors.response.use(
    function (response) {
        // Do something with response data
        return response;
    },
    async function (error) {
        // Do something with response error
        let request = error.config
        console.log(error)
        if (error.response.status === 401 || error.response.status === 403) {
            localStorage.removeItem('auth-token')
            localStorage.removeItem('vuex')
            await router.replace({name: "login"})

        } else {
            return Promise.reject(error);
        }
    }
);


window.axios = api
