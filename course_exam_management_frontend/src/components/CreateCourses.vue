<template>
    <v-row justify="end" class="mt-2 mr-1 mb-2">
        <v-dialog
                v-model="createCourseDialog"
                fullscreen
                :scrim="false"
                transition="dialog-bottom-transition"
        >
            <template v-slot:activator="{ props }">
                <v-btn
                        color="#dc899e"
                        dark
                        v-bind="props"
                        @click="getMe"
                >
                    Create Course
                </v-btn>
            </template>
            <v-card>
                <v-toolbar
                        dark
                        color="#dc899e"
                >
                    <v-btn
                            icon
                            dark
                            @click="createCourseDialog = false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                        <v-toolbar-title v-if="!isEditCourse">Create Course</v-toolbar-title>
                        <v-toolbar-title v-else>Edit Course</v-toolbar-title>
                        <v-spacer></v-spacer>
                    <v-toolbar-items>
                        <v-btn
                                variant="text"
                                @click="createCourseDialog = false"
                        >
                            Save
                        </v-btn>
                    </v-toolbar-items>
                </v-toolbar>
                <v-form @submit.prevent="createCourse" enctype="multipart/form-data">
                    <v-container>
                        <h3>Course Information</h3>
                        <v-row>
                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="name"
                                        label="Name"
                                ></v-text-field>
                                <p v-show="has('name')"
                                   v-text="this.errors['name'] ? this.errors['name'][0]:''"
                                   style="color: red"></p>
                            </v-col>

                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="description"
                                        label="Description"
                                ></v-text-field>
                                <p v-show="has('description')"
                                   v-text="this.errors['description'] ? this.errors['description'][0]:''"
                                   style="color: red"></p>
                            </v-col>
                            <v-col
                                    cols="6"
                            >
                                <VueMultiselect
                                        v-model="classesSelected"
                                        :options="classes"
                                        :multiple="true"
                                        :close-on-select="false"
                                        placeholder="Select Classes"
                                        label="name"
                                        track-by="id"
                                />
                            </v-col>
                            <v-col
                                    cols="6"
                            >
                                <VueMultiselect
                                        v-model="quizSelected"
                                        :options="quizes"
                                        :multiple="true"
                                        :close-on-select="false"
                                        placeholder="Select Quiz"
                                        label="name"
                                        track-by="id"
                                />
                            </v-col>
                            <v-col cols="6">
                                <v-file-input
                                        v-model="show_image"
                                        accept="image/*"
                                        label="Select Course Image"
                                        @change="uploadImage"
                                ></v-file-input>
                            </v-col>
                        </v-row>
                        <v-row justify="center">
                            <v-col cols="6">
                                <v-btn type="submit" color="#dc899e" block class="mt-2" v-if="!isEditCourse">Create
                                    Course
                                </v-btn>
                                <v-btn @click="updateCourse" color="#dc899e" block class="mt-2" v-else>Update Course
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
import router from "@/router";
import store from "@/store";
import {mapGetters} from "vuex";
import {formToJSON} from "axios";
import CreateMCQSPaper from "@/components/CreateMCQSPaper.vue";

export default {
    name: "CreateCourses",
    components: {CreateMCQSPaper, VueMultiselect},
    props: ["isEditCourse", "selectedEditCourse"],
    data() {
        return {
            classes: [],
            classesSelected: [],
            classesIds: [],
            image: null,
            show_image: null,
            createCourseDialog: false,
            created_by: null,
            name: null,
            description: null,
            courseResponse: null,
            errors: [],
            quizes: [],
            quiz: [],
            quizSelected: [],
            // form: new FormData({
            //     students: [],
            //     created_by: null,
            //     name: null,
            //     description: null,
            //     image: this.image,
            // })

        }
    },
    methods: {
        getClasses() {
            api.get('/classes/').then(response => {
                this.classes = response.data
            })
        },
        uploadImage(e) {
            this.image = e.target.files[0]
        },
        createCourse() {
            this.classesIds = []
            this.classesSelected.forEach(student => {
                this.classesIds.push(student.id)
            })
            this.quiz = []
            this.quizSelected.forEach(student => {
                this.quiz.push(student.id)
            })

            let formData = {};

            formData['name'] = this.name;
            formData['description'] = this.description;
            formData['created_by'] = this.created_by;
            formData['classes'] = this.classesIds;
            formData['quiz'] = this.quiz;

            api.post('/courses/', formData,).then(response => {
                this.$emit("update-courses")
                this.courseResponse = response.data
                this.name = null
                this.description = null
                this.students = []
                this.studentsSelected = []
                this.sendImage()
                this.createCourseDialog = false
                this.quiz = null

            }).catch(error => {
                this.errors = error.response.data
            })
        },
        getMe() {
            this.created_by = this.fetchMe.id
            this.emitter.emit('create-class', false)
        },

        sendImage() {
            let formData = {};
            formData['image'] = this.image;
            api.patch('/courses/' + this.courseResponse.id + "/", formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(response => {
                this.image = null
                this.show_image = null
                this.$emit("update-courses")
            }).catch(error => {
                console.log(error)
            })
        },
        has(field) {
            let hasError = this.errors.hasOwnProperty(field);

            if (!hasError) {
                const errors = Object.keys(this.errors).filter(
                    e => e.startsWith(`${field}.`) || e.startsWith(`${field}[`)
                );

                hasError = errors.length > 0;
            }

            return hasError;
        },
        getQuizes() {
            api.get('/quizes/').then(response => {
                this.quizes = response.data
            })
        },

        updateCourse() {
            this.classesIds = []
            this.classesSelected.forEach(student => {
                this.classesIds.push(student.id)
            })
            this.quiz = []
            this.quizSelected.forEach(student => {
                this.quiz.push(student.id)
            })

            let formData = {};

            formData['name'] = this.name;
            formData['description'] = this.description;
            formData['classes'] = this.classesIds;
            formData['quiz'] = this.quiz;

            api.patch('/courses/' + this.selectedEditCourse.id + "/", formData,).then(response => {
                this.$emit("update-courses")
                this.courseResponse = response.data
                this.name = null
                this.description = null
                this.students = []
                this.studentsSelected = []
                this.sendImage()
                this.createCourseDialog = false
                this.quiz = null

            }).catch(error => {
                this.errors = error.response.data
            })
        },


    },
    computed: {
        ...mapGetters([
            'fetchMe',
        ])

    },
    watch: {
        selectedEditCourse: function (newVal, oldVal) {
            if (this.isEditCourse) {
                this.createCourseDialog = true
                console.log(newVal)
                this.name = newVal.name
                this.description = newVal.description
                this.quizSelected = newVal.quiz_detail
                this.classesSelected = newVal.classes_detail
            }
        }
    },
    mounted() {
        this.getClasses()
        this.getQuizes()
    }
}
</script>

<style scoped>
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
    transition: transform .2s ease-in-out;
}
</style>
