<template>
    <v-card class="mt-3 ml-3 mr-3">
        <v-card-title>
            <span class="text-h5">Forgot Password</span>
        </v-card-title>
        <v-card-text>
            <v-container>
                <v-row>
                    <v-col
                            cols="6"
                    >
                        <v-text-field
                                label="Email"
                                v-model="form.email"
                                type="email"
                        ></v-text-field>
                        <div class="v-messages v-messages__message" v-show="form.errors.has('email')"
                             v-text="form.getError('email')" style="color: red"></div>
                    </v-col>
                    <v-col
                            cols="6"
                    >
                        <v-text-field
                                label="New Password"
                                v-model="form.password"
                                type="password"
                        ></v-text-field>
                        <div class="v-messages v-messages__message" v-show="form.errors.has('password')"
                             v-text="form.getError('password')" style="color: red"></div>
                    </v-col>

                </v-row>
                <v-row justify="center">
                    <v-col cols="6">
                        <v-btn type="submit" color="primary" block class="mt-2" @click="changePassword">Change
                            Password
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-card-text>
    </v-card>
</template>

<script>
import Form from "@/utils/form";
import router from "@/router";

export default {
    name: "ChangePassword",
    data() {
        return {
            form: new Form({
                email: null,
                password: null
            }),
        }
    },
    methods: {
        changePassword() {
            this.form.submit('post', 'users/password_reset/').then(response => {
                router.push('/login')
            })
        }
    }

}
</script>

<style scoped>

</style>
