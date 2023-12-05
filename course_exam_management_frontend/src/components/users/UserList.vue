<template>
    <v-container>
        <h2 class="mb-3">Users</h2>
        <v-data-table
                v-model:items-per-page="itemsPerPage"
                :headers="headers"
                :items="users"
                item-value="name"
                class="elevation-1"
        >

            <template v-slot:top>
                <v-toolbar
                        flat
                >
                    <v-toolbar-title>Users</v-toolbar-title>

                    <v-spacer></v-spacer>
                    <v-btn
                            color="primary"
                            class="mb-2 justify-end"
                            @click="openUserForm"
                    >
                        New User
                    </v-btn>


                </v-toolbar>
                <CreateUser :create-user-dialog="createUserDialogValue"
                            @update-create-user-dialog-value="updateUserDialogValue"/>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn-group density="compact">
                    <v-btn color="#dc899e" @click="editUser(item.raw)">Edit</v-btn>&nbsp;
                    <v-btn color="secondary" @click="updateUser(item.raw)" v-if="!item.raw.is_active">Activate</v-btn>
                    <v-btn color="secondary" @click="updateUser(item.raw)" v-else>Deactivate</v-btn>
                </v-btn-group>
            </template>
            <template v-slot:item.is_active="{ item }">
                <span v-if="item.raw.is_active">True</span>
                <span v-else>False</span>
            </template>
                        <template v-slot:item.is_student="{ item }">
                        <span v-if="item.raw.is_student">Student</span>
                        <span v-else-if="item.raw.username === 'Administrator'">Administrator</span>
                        <span v-else>Teacher</span>
                    </template>
        </v-data-table>
    </v-container>
</template>

<script>
import {VDataTable} from "vuetify/lib/labs/VDataTable";
import {api} from "@/utils/axios";
import CreateUser from "@/components/users/CreateUser.vue";

export default {
    name: "UserList",
    components: {CreateUser, VDataTable},
    data() {
        return {
            itemsPerPage: 10,
            users: [],
            createUserDialogValue: false,
            headers: [
                {
                    title: 'Username',
                    align: 'start',
                    sortable: false,
                    key: 'username',
                },
                {title: 'Email', align: 'start', key: 'email'},
                {title: 'User Active', align: 'start', key: 'is_active'},
                { title: 'Type', align: 'start', key: 'is_student' },
                { title: 'Actions', key: 'actions', sortable: false },
            ],
        }
    },
    methods: {
        getUsers() {
            api.get('/users/').then(response => {
                this.users = response.data
            })
        },
        updateUserDialogValue(value) {
            this.createUserDialogValue = value
            this.getUsers()
        },
        openUserForm() {
            this.emitter.emit("create-user")
            this.createUserDialogValue = true
        },
        editUser(classObj) {
            this.createUserDialogValue = true
            this.emitter.emit("edit-user", classObj)

        },
        updateUser(user) {
            // user.is_active = !user.is_active
            axios.patch('/users/' + user.id + "/", {is_active: !user.is_active}).then(response => {
                this.getUsers()

            }).catch(error => {

            })
        },
        // deleteClass(obj) {
        //     api.delete('/classes/' + obj.id + "/").then(response => {
        //         this.getClass()
        //     })
        // },

    },

    mounted() {
        this.getUsers()
    },
}
</script>

<style scoped>

</style>
