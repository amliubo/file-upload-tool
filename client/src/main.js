import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import 'bootstrap/dist/css/bootstrap.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import SvgIcon from './components/SvgIcon.vue'
import './assets/iconfont.js'
const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue, SvgIcon)) {
    app.component(key, component)
}
app.use(router)
app.use(ElementPlus)
app.mount('#app')
