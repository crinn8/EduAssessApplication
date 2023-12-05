<template>
    <v-row justify="end" class="mt-2 mr-1 mb-2">
        <v-dialog
                v-model="createUserDialogCompute"
                fullscreen
                :scrim="false"
                transition="dialog-bottom-transition"
        >

            <v-card>
                <v-toolbar
                        dark
                        color="#dc899e"
                >
                    <v-btn
                            icon
                            dark
                            @click="createUserDialogCompute = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title v-if="!isUserEdit">Create User</v-toolbar-title>
                        <v-toolbar-title v-else>Edit User</v-toolbar-title>
                        <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                                variant="text"
                                @click="createUserDialogCompute = false"
                        >
                            Save
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>
                <v-form @submit.prevent="createUser">
                    <v-container>
                        <h3>User Information</h3>
                        <v-row>
                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="form.username"
                                        label="Username"
                                ></v-text-field>
                                <div class="v-messages v-messages__message" v-show="form.errors.has('username')"
                                     v-text="form.getError('username')" style="color: red"></div>
                            </v-col>
                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="form.email"
                                        label="Email"
                                ></v-text-field>
                                <div class="v-messages v-messages__message" v-show="form.errors.has('email')"
                                     v-text="form.getError('email')" style="color: red"></div>
                            </v-col>
                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="form.password"
                                        label="Password"
                                ></v-text-field>
                                <div class="v-messages v-messages__message" v-show="form.errors.has('password')"
                                     v-text="form.getError('password')" style="color: red"></div>
                            </v-col>
                            <v-col
                                    cols="6"
                                    v-if="!isUserEdit"
                            >
                                <v-checkbox v-model="form.is_student" label="Is Student"
                                ></v-checkbox>
                            </v-col>
                                            <v-col cols="6">
                        <v-radio-group v-model="form.gender" row>
                            <v-radio label="Female" value="female"></v-radio>
                            <v-radio label="Male" value="male"></v-radio>
                        </v-radio-group>
                    </v-col>
                    <v-col cols="6">
                        <v-btn color="#dc899e" block class="mt-2" @click="generateAvatar">Generate Avatar</v-btn>
                            <div v-if="form.avatar">
                                <img :src="form.avatar" alt="Avatar" class="mt-2" />
                            </div> 
                    </v-col>
                       

                        </v-row>
                        <v-row justify="center">
                            <v-col cols="6">
                                <v-btn type="submit" color="#dc899e" block class="mt-2" v-if="!isUserEdit">Create
                                    User
                                </v-btn>
                                <v-btn color="#dc899e" block class="mt-2" v-else @click="updateUser">Update User
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-container>

                </v-form>

            </v-card>


        </v-dialog>
    </v-row>
</template>

<script>
import Form from "@/utils/form";
import {mapGetters} from "vuex";
import { api } from "@/utils/axios";
import store from "@/store";

const axios = require('axios');
let url_image =  null;

export default {
    name: "CreateUser",
    props: [
        "createUserDialog"
    ],
    data() {
        return {
            createUserDialogValue: false,
            isUserEdit: false,
            userEditId: null,

            form: new Form({
                username: null,
                email: null,
                password: null,
                is_student: false,
                image: null
            })
        }
    },
    methods: {
        createUser() {
            this.form.image = url_image
            this.form.submit('post', '/users/').then(response => {
                this.$emit('update-create-user-dialog-value', false)
                this.form.reset()

            }).catch(error => {
                console.log(error)
            })
        },

        setGender(gender) {
            this.gender = gender;
        },
        updateUser() {
            this.form.image = url_image
            this.form.submit('patch', '/users/' + this.userEditId + "/").then(response => {
                this.$emit('update-create-user-dialog-value', false)
                this.form.reset()
                this.isUserEdit = false

            }).catch(error => {

            })
        },
        getMe() {
            this.created_by = this.fetchMe.id
        },
        async generateAvatar() {
            var prompt = "";
            if (this.form.gender == "male") {
                if (this.form.is_student)
                    prompt = "A student boy avatar";
                else
                    prompt = "A teacher men avatar";
            }
            else if (this.form.gender == "female") {
                if (this.form.is_student)
                    prompt = "A student girl avatar";
                else
                    prompt = "A teacher women avatar";
            }
            const numberOfImages = 1;
            const imageSize = "256x256";

            const response = await axios.post('https://api.openai.com/v1/images/generations', {
                prompt: prompt,
                n: numberOfImages,
                size: imageSize,
            }, {
                headers: {
                    'Authorization': 'Bearer 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',
                },
            });
            console.log(response.data.data[0]['url']);
            const encodedParams = new URLSearchParams();
            encodedParams.set('url', response.data.data[0]['url'] );

            const options = {
                method: 'POST',
                url: 'https://url-shortener-service.p.rapidapi.com/shorten',
                headers: {
                    'content-type': 'application/x-www-form-urlencoded',
                    'X-RapidAPI-Key': '941f880893msh47bc9f650c86d31p1ded61jsn5b5682bbe6b8',
                    'X-RapidAPI-Host': 'url-shortener-service.p.rapidapi.com'
                },
                data: encodedParams,
            };

            try {
                const response1 = await axios.request(options);
                url_image = response1.data['result_url'];
                console.log(url_image);
            } catch (error) {
                console.error(error);
            }

            this.form.avatar = response.data.data[0]['url'];
        },


    },
    computed: {
        ...mapGetters([
            'fetchMe',
        ]),
        createUserDialogCompute: {
            get() {
                this.createUserDialogValue = this.createUserDialog
                return this.createUserDialogValue
            },
            set(value) {
                console.log(value)
                this.$emit('update-create-user-dialog-value', value)
            }
        }

    },
    created() {
        this.emitter.on("edit-user", (classObj) => {
            this.form.username = classObj.username
            this.form.email = classObj.email
            this.form.is_student = classObj.is_student
            this.userEditId = classObj.id
            this.isUserEdit = true
        })

        this.emitter.on("create-user", (classObj) => {
            this.isUserEdit = false
        })
    }

}
</script>

