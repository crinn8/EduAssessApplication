<template>

    <v-container>

        <CreateCourses @update-courses="getCourses" :is-edit-course="isEditCourse"
                       :selected-edit-course="selectedEditCourse"/>

        <h2 class="mb-3">Courses</h2>

        <v-row v-if="courses.length===0">
            <v-col cols="12" class="d-flex justify-center align-center">
                No Courses Exist
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col
                    v-for="course in courses"
                    :key="course.id"
                    :cols="4"
            >
                <v-card>
                    <v-img
                            :src="course.image"
                            class="align-end"
                            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                            height="200px"
                            cover
                    >
                        <v-card-title class="text-white" v-text="course.name"></v-card-title>
                    </v-img>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn size="small" color="surface-variant" variant="text" icon="mdi-eye-circle-outline"
                               @click="courseDetail(course.id)"></v-btn>
                        <v-btn size="small" color="surface-variant" variant="text" icon="mdi-pencil"
                               @click="editCourse(course)"></v-btn>
                        <v-btn size="small" color="surface-variant" variant="text" icon="mdi-delete"
                               @click="deleteCourse(course)"></v-btn>


                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>

    </v-container>
    <delete-model/>

</template>

<script>
import {api} from "@/utils/axios";
import CreateCourses from "@/components/CreateCourses.vue";
import router from "@/router";
import DeleteModel from "@/components/common/DeleteModel.vue";

export default {
    name: "TeacherCourses",
    components: {DeleteModel, CreateCourses},
    data() {
        return {
            courses: [],
            createCourseDialog: false,
            isEditCourse: false,
            selectedEditCourse: {}
        }
    },
    methods: {
        getCourses() {
            api.get('/courses/').then(response => {
                this.courses = response.data
            })
        },
        courseDetail(id) {
            router.push({name: 'courses_detail', params: {id: id}})
        },
        editCourse(course) {
            this.isEditCourse = true
            this.selectedEditCourse = course
        },
        deleteCourse(course) {
            this.emitter.emit("delete-record", '/courses/' + course.id + "/")
        },
    },
    mounted() {
        this.getCourses()
    },
    created() {
        this.emitter.on("create-class", (value) => {
            this.isEditCourse = value
            this.selectedEditCourse = {}
        })
        this.emitter.on("record-deleted", () => {
            this.getCourses()
        })
    }
}
</script>

<style scoped>

</style>
