<template>
    <v-container>
        <v-card class="mt-2 mb-2 ml-2 mr-2">
            <v-card-title>Course Detail</v-card-title>
            <v-row class="ma-2">
                <h4>Course Name: {{ results.name }}</h4>
            </v-row>
            <v-row class="ma-2">
                <h4>Description: {{ results.description }}</h4>
            </v-row>
            <v-row class="ma-2 mt-5 pt-5">
                <v-file-input
                        label="Upload Files"
                        @change="uploadImage"
                ></v-file-input>
                <v-btn class="ml-5 mt-3" color="#dc899e" @click="sendFiles">Upload</v-btn>

            </v-row>

            <v-table>
                <thead>
                <tr>
                    <th class="text-left">
                        Course Files
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr
                        v-for="result in courseFiles"
                        :key="result.id"
                >
                    <td><a :href="result.file"
                           target="_blank">{{ result.file }}</a></td>
                    <td>
                        <v-btn-group density="compact">
                            <v-btn color="#dc899e" @click="downloadFile(result.file)">Download</v-btn>&nbsp;
                            <v-btn color="#ce5a5a" @click="deleteFile(result.id)">Delete</v-btn>
                        </v-btn-group>

                    </td>

                </tr>
                </tbody>
            </v-table>
        </v-card>
    </v-container>
</template>

<script>
import {api} from "@/utils/axios";
import {saveAs} from 'file-saver';

export default {
    name: "CourseDetail",
    data() {
        return {
            results: [],
            courseFiles: [],
            files: null,
        }
    },
    methods: {
        getResult() {
            api.get('/delivered_quiz/?course__id=' + this.$route.params.id).then(response => {
                this.results = response.data
            })
        },
        uploadImage(e) {
            console.log(e.target.files)
            this.files = e.target.files[0]
        },
        getCourseDetail() {
            api.get('/courses/' + this.$route.params.id + "/").then(response => {
                this.results = response.data
            })
        },

        getCourseFiles() {
            api.get('/course-files/?course__id=' + this.$route.params.id).then(response => {
                this.courseFiles = response.data
            })
        },
        sendFiles() {
            let formData = {};
            formData['file'] = this.files;
            formData['course'] = this.$route.params.id;
            api.post('/course-files/', formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(response => {
                this.getCourseFiles()
                this.files = null
            }).catch(error => {
                console.log(error)
            })
        },
        async downloadFile(url) {
            const fileUrl = url; // Replace with your file URL
            try {
                const response = await axios.get(fileUrl, {responseType: 'blob'});
                const fileName = 'file.pdf'; // Specify the desired filename for the downloaded file
                saveAs(response.data, url.split("/")[url.split("/").length - 1]);
            } catch (error) {
                console.error('Error downloading file:', error);
            }
        },
        deleteFile(id) {
            api.delete('/course-files/' + id + "/").then(response => {
                this.getCourseFiles()
            })
        }
    },
    mounted() {
        this.getCourseDetail()
        this.getCourseFiles()

    }
}
</script>

<style scoped>

</style>
