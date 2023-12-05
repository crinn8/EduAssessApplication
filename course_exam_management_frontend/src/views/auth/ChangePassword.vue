<template>
    <v-card class="mt-3 ml-3 mr-3">
        <v-card-title>
            <span class="text-h5">Change Password</span>
        </v-card-title>
        <v-card-text>
            <v-container>
                <v-row>
                    <v-col
                            cols="6"
                    >
                        <v-text-field
                                label="Old Password"
                                v-model="form.old_password"
                        ></v-text-field>
                        <div class="v-messages v-messages__message" v-show="form.errors.has('old_password')"
                             v-text="form.getError('old_password')" style="color: red"></div>
                    </v-col>
                    <v-col
                            cols="6"
                    >
                        <v-text-field
                                label="New Password"
                                v-model="form.new_password"
                        ></v-text-field>
                        <div class="v-messages v-messages__message" v-show="form.errors.has('new_password')"
                             v-text="form.getError('new_password')" style="color: red"></div>
                    </v-col>
                    <v-col
                            cols="6"
                    >
                        <v-text-field
                                label="Confirm Password"
                                v-model="form.confirm_password"

                        ></v-text-field>
                        <div class="v-messages v-messages__message" v-show="form.errors.has('confirm_password')"
                             v-text="form.getError('confirm_password')" style="color: red"></div>
                    </v-col>

                </v-row>
                <v-row justify="center">
                    <v-col cols="6">
                        <v-btn type="submit" color="#dc899e" block class="mt-2" @click="changePassword">Change
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

export default {
    name: "ChangePassword",
    data() {
        return {
            form: new Form({
                old_password: null,
                new_password: null,
                confirm_password: null
            }),
        }
    },
    methods: {
        changePassword() {
            this.form.submit('put', '/change-password/').then(response => {

            })
        }
    }

}
</script>

<style scoped>

</style>
