<template>
    <v-container>
        <!--        <CreateCourses @update-courses="getCourses"/>-->

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

                        <v-btn size="small" color="surface-variant" variant="text"
                               @click="startQuiz(course)">Quizzes
                        </v-btn>
                        <v-btn size="small" color="surface-variant" variant="text" icon="mdi-eye-circle-outline"
                               @click="courseDetail(course.id)"></v-btn>
                        <v-btn size="small" color="surface-variant" variant="text" icon="mdi-bookmark"></v-btn>

                        <!--                        <v-btn size="small" color="surface-variant" variant="text"-->
                        <!--                               icon="mdi-share-variant"></v-btn>-->
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>

    </v-container>

</template>

<script>

import {api} from "@/utils/axios";
import {mapGetters} from "vuex";
import router from "@/router";

export default {
    name: "StudentCourses",
    data() {
        return {
            courses: [],
        }
    },
    methods: {
        getCourses() {
            api.get('/courses/?classes__students__id=' + this.fetchMe.id).then(response => {
                this.courses = response.data
            })
        },
        startQuiz(course) {
            router.push({name: 'start_quiz', params: {id: course.id}})
        },
        courseDetail(id) {
            router.push({name: 'student_courses_detail', params: {id: id}})
        },
    },
    computed: {
        ...mapGetters([
            'fetchMe',
        ])

    },
    mounted() {
        this.getCourses()
    },
}
</script>

<style scoped>

</style>
