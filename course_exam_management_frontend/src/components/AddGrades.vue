<template>
    <v-row justify="end" class="mt-2 mr-1 mb-2">
        <v-dialog
                v-model="createGradeDialogCompute"
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
                            @click="createGradeDialogCompute = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                        <v-toolbar-title v-if="!isGradeEdit">Add Grade</v-toolbar-title>
                        <v-toolbar-title v-else>Edit Grade</v-toolbar-title>
                        <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                                variant="text"
                                @click="createGradeDialogCompute = false"
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
                                        v-model="form.total_numbers"
                                        type="number"
                                        label="Total Number"
                                ></v-text-field>
                                <div class="v-messages v-messages__message" v-show="form.errors.has('total_numbers')"
                                     v-text="form.getError('total_numbers')" style="color: red"></div>
                            </v-col>
                            <v-col
                                    cols="6"
                            >
                                <VueMultiselect
                                        v-model="studentsSelected"
                                        :options="users"
                                        :multiple="false"
                                        :close-on-select="true"
                                        placeholder="Select Student"
                                        label="email"
                                        track-by="id"
                                />
                                <div class="v-messages v-messages__message" v-show="form.errors.has('student')"
                                     v-text="form.getError('student')" style="color: red"></div>
                            </v-col>

                            <v-col
                                    cols="6"
                            >
                                <VueMultiselect
                                        v-model="courseSelected"
                                        :options="courses"
                                        :multiple="false"
                                        :close-on-select="true"
                                        placeholder="Select Course"
                                        label="name"
                                        track-by="id"
                                />
                                <div class="v-messages v-messages__message" v-show="form.errors.has('course')"
                                     v-text="form.getError('course')" style="color: red"></div>
                            </v-col>


                        </v-row>
                        <v-row justify="center">
                            <v-col cols="6">
                                <v-btn type="submit" color="#dc899e" block class="mt-2" v-if="!isGradeEdit">Add
                                    Grade
                                </v-btn>
                                <v-btn color="#dc899e" block class="mt-2" v-else @click="updateClass">Update Grade
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
        "createGradeDialog"
    ],
    components: {CreateMCQSPaper, VueMultiselect},
    data() {
        return {
            users: [],
            studentsSelected: {},
            courseSelected: {},
            quizSelected: {},
            createGradeDialogValue: false,
            isGradeEdit: false,
            gradeEditId: null,
            courses: [],
            quizes: [],

            form: new Form({
                student: null,
                quiz: null,
                course: null,
                total_numbers: 0,
                is_custom_add: true
            })

        }
    },
    methods: {
        getUsers() {
            api.get('/users/?is_student=true').then(response => {
                this.users = response.data
            })
        },
        getQuizes() {
            api.get('/quizes/').then(response => {
                this.quizes = response.data
            })
        },
        getCourse() {
            api.get('/courses/').then(response => {
                this.courses = response.data
            })
        },
        createClass() {
            this.form.student = this.studentsSelected.id
            this.form.course = this.courseSelected.id
            this.form.quiz = this.quizSelected.id


            this.form.submit('post', '/delivered-quizes/').then(response => {
                this.$emit('update-create-grade-dialog-value', false)
                this.form.reset()
                this.studentsSelected = {}
                this.courseSelected = {}
                this.quizSelected = {}

            }).catch(error => {

            })
        },
        updateClass() {
            this.form.student = this.studentsSelected.id
            this.form.course = this.courseSelected.id
            this.form.quiz = this.quizSelected.id


            this.form.submit('patch', '/delivered-quizes/' + this.gradeEditId + "/").then(response => {
                this.$emit('update-create-grade-dialog-value', false)
                this.form.reset()
                this.studentsSelected = {}
                this.courseSelected = {}
                this.quizSelected = {}
                this.isGradeEdit = false

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
        createGradeDialogCompute: {
            get() {
                this.createGradeDialogValue = this.createGradeDialog
                return this.createGradeDialogValue
            },
            set(value) {
                console.log(value)
                this.$emit('update-create-grade-dialog-value', value)
            }
        }

    },
    mounted() {
        this.getUsers()
        this.getQuizes()
        this.getCourse()
    },
    created() {
        this.emitter.on("edit-grade", (classObj) => {
            this.studentsSelected = classObj.students_detail
            this.courseSelected = classObj.course_detail
            this.quizSelected = classObj.quiz_detail
            this.form.total_numbers = classObj.total_numbers
            this.gradeEditId = classObj.id
            this.isGradeEdit = true


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
