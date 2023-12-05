<template>
    <div :style="{ 'background-image': 'url(' + require('@/assets/lV9LYT.jpg') + ')' }" class="image">
        <v-row>
            <v-col cols="4" style="color: #0C0B0BFF; margin-left: 90px;" class="mt-16">
                <v-row class="mt-16 ml-16">

                    <v-col cols="11" class="pt-15">
                        <h1 class="ml-16 mb-4 pl-14">LOGIN</h1>
                        <v-form fast-fail @submit.prevent="login">
                            <v-text-field variant="outlined" v-model="form.username" label="Email"></v-text-field>

                            <v-text-field type="password" variant="outlined" v-model="form.password"
                                label="Password"></v-text-field>
                            <p v-show="form.errors.has('non_field_errors')" v-text="form.getError('non_field_errors')"
                                style="color: red"></p>

                            <v-btn type="submit" color="#dc899e" block class="mt-2">Sign in</v-btn>

                        </v-form>

                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </div>
</template>

<script>


import {api} from "@/utils/axios";
import Form from "@/utils/form";
import router from "@/router";
import store from "@/store";

export default {
    name: "Login",
    data() {
        return {

            form: new Form({
                username: "",
                password: "",
            })
        }
    },
    methods: {
        login() {
            localStorage.setItem('auth-token', "")
            this.form.submit('post', '/auth-token/').then(response => {

                localStorage.setItem('auth-token', response.token)
                store.dispatch("getMe")
                // router.push('/')
            })
        }
    }
}
</script>

<style scoped>
.image {
    height: 100%;

    /* Center and scale the image nicely */
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}

</style>
