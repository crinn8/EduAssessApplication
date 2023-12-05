<template>
    <v-row justify="center">
        <v-dialog
                v-model="dialog"
                persistent
                width="auto"
        >
            <v-card>
                <v-card-title class="text-h5">
                    Delete Record
                </v-card-title>
                <v-card-text>Are you sure you want to delete this record?</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                            color="green-darken-1"
                            variant="text"
                            @click="dialog = false"
                    >
                        Cancel
                    </v-btn>
                    <v-btn
                            color="red"
                            variant="text"
                            @click="deleteRecord"
                    >
                        Confirm
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
import {api} from "@/utils/axios";

export default {
    name: "DeleteModel",
    data() {
        return {
            dialog: false,
            url: null
        }
    },
    methods: {
        deleteRecord() {
            this.dialog = false
            api.delete(this.url).then(response => {
                this.emitter.emit("record-deleted")
            })
        },
    },
    created() {
        this.emitter.on("delete-record", (url) => {
            this.url = url
            this.dialog = true
        })
    }

}
</script>

<style scoped>

</style>
