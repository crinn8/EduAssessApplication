import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import '@mdi/font/css/materialdesignicons.css'
import '@mdi/js'
import 'vue-multiselect/dist/vue-multiselect.css'

// Vuetify
import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import mitt from 'mitt'
import {install as VueMonacoEditorPlugin} from '@guolao/vue-monaco-editor'
import "vuepython/style.css";
import "highlight.js/styles/stackoverflow-light.css"

const emitter = mitt()

const vuetify = createVuetify({
    icons: {
        iconfont: 'mdiSvg', // default - only for display purposes
    },
    components,
    directives,
})
const app = createApp(App)
app.config.globalProperties.emitter = emitter
app.use(store).use(router).use(vuetify).use(VueMonacoEditorPlugin).mount('#app')
