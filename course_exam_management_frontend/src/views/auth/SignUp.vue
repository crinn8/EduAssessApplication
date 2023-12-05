<template>
    <div class="d-flex align-center justify-center" style="height: 100vh">
        <v-sheet width="400" class="mx-auto">
            <v-form fast-fail @submit.prevent="login">
                <v-text-field variant="outlined" v-model="form.email" label="Email"></v-text-field>
                <p v-show="form.errors.has('email')" v-text="form.getError('email')" style="color: red"></p>
                <v-text-field variant="outlined" v-model="form.username" label="User Name"></v-text-field>
                <p v-show="form.errors.has('username')" v-text="form.getError('username')" style="color: red"></p>
                <v-text-field type="password" variant="outlined" v-model="form.password"
                              label="password"></v-text-field>
                <p v-show="form.errors.has('password')"
                   v-text="form.getError('password')" style="color: red"></p>
                <v-checkbox v-model="form.is_student" label="Are you a Student"></v-checkbox>

                <v-btn type="submit" color="primary" block class="mt-2">Sign Up</v-btn>

            </v-form>
            <div class="mt-2">
                <p class="text-body-2">Don't have an account? <a href="login">Login In</a></p>
            </div>
        </v-sheet>
    </div>
</template>

<script>


import {api} from "@/utils/axios";
import Form from "@/utils/form";
import router from "@/router";

export default {
    name: "SignUp",
    data() {
        return {

            form: new Form({
                username: "",
                password: "",
                email: "",
                is_student: false,
            })
        }
    },
    methods: {
        login() {
            this.form.submit('post', '/auth/users/').then(response => {
                router.push('/login')
            })
        }
    }
}
</script>

<style scoped>

</style>
