<template>
    <v-row justify="end" class="mt-2 mr-1 mb-2">
        <v-dialog
                v-model="createClassDialogCompute"
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
                            @click="createClassDialogCompute = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                        <v-toolbar-title v-if="!isClassEdit">Create Class</v-toolbar-title>
                        <v-toolbar-title v-else>Edit Class</v-toolbar-title>
                        <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                                variant="text"
                                @click="createClassDialogCompute = false"
                        >
                            Save
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>
                <v-form @submit.prevent="createClass">
                    <v-container>
                        <h3>Class Information</h3>
                        <v-row>
                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="form.name"
                                        label="Name"
                                ></v-text-field>
                                <div class="v-messages v-messages__message" v-show="form.errors.has('name')"
                                     v-text="form.getError('name')" style="color: red"></div>
                            </v-col>
                            <v-col
                                    cols="6"
                            >
                                <VueMultiselect
                                        v-model="studentsSelected"
                                        :options="users"
                                        :multiple="true"
                                        :close-on-select="false"
                                        placeholder="Select Student"
                                        label="email"
                                        track-by="id"
                                />
                                <div class="v-messages v-messages__message" v-show="form.errors.has('students')"
                                     v-text="form.getError('students')" style="color: red"></div>
                            </v-col>

                        </v-row>
                        <v-row justify="center">
                            <v-col cols="6">
                                    <v-btn type="submit" color="#dc899e" block class="mt-2" v-if="!isClassEdit">Create
                                        Class
                                    </v-btn>
                                    <v-btn color="#dc899e" block class="mt-2" v-else @click="updateClass">Update Class
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
import {api} from "@/utils/axios";
import VueMultiselect from 'vue-multiselect'
import {mapGetters} from "vuex";
import CreateMCQSPaper from "@/components/CreateMCQSPaper.vue";

export default {
    name: "CreateClass",
    props: [
        "createClassDialog"
    ],
    components: {CreateMCQSPaper, VueMultiselect},
    data() {
        return {
            users: [],
            studentsSelected: [],
            createClassDialogValue: false,
            isClassEdit: false,
            classEditId: null,

            form: new Form({
                students: [],
                created_by: null,
                name: null
            })

        }
    },
    methods: {
        getUsers() {
            api.get('/users/?is_student=true').then(response => {
                this.users = response.data
            })
        },
        createClass() {
            this.form.students = []
            this.studentsSelected.forEach(student => {
                this.form.students.push(student.id)
            })
            this.form.created_by = this.fetchMe.id


            this.form.submit('post', '/classes/').then(response => {
                this.$emit('update-create-class-dialog-value', false)
                this.form.reset()
                this.studentsSelected = []

            }).catch(error => {

            })
        },
        updateClass() {
            this.form.students = []
            this.studentsSelected.forEach(student => {
                this.form.students.push(student.id)
            })
            this.form.created_by = this.fetchMe.id


            this.form.submit('patch', '/classes/' + this.classEditId + "/").then(response => {
                this.$emit('update-create-class-dialog-value', false)
                this.form.reset()
                this.studentsSelected = []
                this.isClassEdit = false

            }).catch(error => {

            })
        },
        getMe() {
            this.created_by = this.fetchMe.id
        },


    },
    // watch: {
    //     createClassDialog: function (newVal, oldVal) {
    //         console.log(newVal)
    //         console.log(oldVal)
    //     }
    // },
    computed: {
        ...mapGetters([
            'fetchMe',
        ]),
        createClassDialogCompute: {
            get() {
                this.createClassDialogValue = this.createClassDialog
                return this.createClassDialogValue
            },
            set(value) {
                console.log(value)
                this.$emit('update-create-class-dialog-value', value)
            }
        }

    },
    mounted() {
        this.getUsers()
    },
    created() {
        this.emitter.on("edit-class", (classObj) => {
            this.studentsSelected = classObj.students_detail
            this.form.name = classObj.name
            this.classEditId = classObj.id
            this.isClassEdit = true


        })
    }

}
</script>

<style scoped>
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
    transition: transform .2s ease-in-out;
}
</style>
