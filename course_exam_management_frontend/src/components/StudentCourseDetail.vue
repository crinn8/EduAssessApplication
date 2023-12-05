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
                        v-for="result in results.course_files"
                        :key="result.id"
                >
                    <td><a :href="result.file"
                           target="_blank">{{ result.file }}</a></td>
                    <td>
                        <v-btn-group density="compact">
                            <v-btn color="#dc899e" @click="downloadFile(result.file)">Download</v-btn>
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
    name: "StudentCourseDetail",
    data() {
        return {
            results: {}
        }
    },
    methods: {
        getCourseDetail() {
            api.get('/courses/' + this.$route.params.id + "/").then(response => {
                this.results = response.data
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
    },
    mounted() {
        this.getCourseDetail()
    }
}
</script>

<style scoped>

</style>
