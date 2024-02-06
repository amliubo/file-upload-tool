<template>
  <div class="container">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-sub-menu index="1">
        <template #title>
          <div v-if="filesBadgeValue > 0">
            <el-badge :value="filesBadgeValue" class="item" type="success">
              <span style="font-size: 16px;"><el-icon>
                  <Folder />
                </el-icon>文件</span>
            </el-badge>
          </div>
          <div v-else>
            <span style="font-size: 16px;"><el-icon>
                <Folder />
              </el-icon>文件</span>
          </div>
        </template>
        <el-menu-item index="1-1" style="font-size: 15px;"><el-icon>
            <ElementPlus />
          </el-icon>组件方式</el-menu-item>
        <el-menu-item index="1-2" style="font-size: 15px;">非组件方式</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="2" style="font-size: 16px;">
        <el-badge value="hot" class="item"><el-icon>
            <Tickets />
          </el-icon>文本</el-badge>
      </el-menu-item>
    </el-menu>
    <br>
    <div v-show="activeIndex === '1-1'">
      <div class="jumbotron jumbotron-fluid">
        <div class="container">
          <div class="header">
            <div>
              <el-divider content-position="left">
                <el-tag class="mx-1" type="success" round>
                  <h1 class="display-4">Upload Tool</h1>
                </el-tag>
              </el-divider>
              <br>
              <p class="lead">这是一个轻量级、安全的文件传输效率工具，支持通过组件方式或非组件方式上传文件，提供实时文件列表和下载功能。</p>
            </div>
            <img src="http://10.10.25.66/resource/erweima.png" class="erweima" v-if="!isMobile">
          </div>
        </div>
      </div>
      <el-upload class="upload-demo" drag action="http://10.10.243.201:5001/upload" multiple :on-success="fetchServerFiles">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖放到此处或<em>单击上传</em>
        </div>
      </el-upload>
      <br>
      <div class="container">
        <el-divider content-position="right">
          <el-tag class="mx-1" type="warning" round>
            <h4 class="display-6" style="text-align: right">File Download</h4>
          </el-tag>
        </el-divider>
        <template v-if="serverFiles.length > 0">
          <ul>
            <li v-for="(file, index) in serverFiles" :key="index">
              <div style="display: flex; align-items: center;">
                <div style="flex: 100%;">
                  <a :href="getDownloadLink(file.name)" :download="file.name" viewer>
                    <span style="font-size: 18px;">{{ file.name }} ({{ formatBytes(file.size) }})</span>
                  </a>
                </div>
                <div style="flex: 38%;">
                  <el-progress status="error" striped striped-flow :stroke-width="1"
                    :percentage="calculateProgress(file.remainingTime)" color="red" />
                </div>
              </div>
            </li>
          </ul>
        </template>
        <template v-else>
          <p class="lead">当前没有可供下载的文件。</p>
        </template>
      </div>
    </div>
    <div v-show="activeIndex === '1-2'">
      <div class="jumbotron jumbotron-fluid">
        <div class="container">
          <div class="header">
            <div>
              <el-divider content-position="left">
                <el-tag class="mx-1" type="success" round>
                  <h1 class="display-4">Upload Tool</h1>
                </el-tag>
              </el-divider>
              <br>
              <p class="lead">这是一个轻量级、安全的文件传输效率工具，支持通过组件方式或非组件方式上传文件，提供实时文件列表和下载功能。</p>
            </div>
            <img src="http://10.10.25.66/resource/erweima.png" class="erweima" v-if="!isMobile">
          </div>
        </div>
      </div>
      <input type="file" ref="fileInput" @change="handleFileChange" multiple />
      <div v-if="selectedFiles && selectedFiles.length > 0">
        <hr>
        <h5>Selected Files:</h5>
        <ul>
          <li v-for="( file, index ) in  selectedFiles " :key="index">
            {{ file.name }} ({{ formatBytes(file.size) }})
          </li>
        </ul>
      </div>
      <button type="button" class="btn btn-primary" @click="handleUpload"
        :disabled="!selectedFiles || selectedFiles.length === 0 || uploading">
        <span v-if="!uploading">Upload Files</span>
        <span v-else>Loading...</span>
      </button>
      <div class="container">
        <br><br><br>
        <el-divider content-position="right">
          <el-tag class="mx-1" type="warning" round>
            <h4 class="display-6" style="text-align: right">File Download</h4>
          </el-tag>
        </el-divider>
        <template v-if="serverFiles.length > 0">
          <ul>
            <li v-for="( file, index ) in  serverFiles " :key="index">
              <a :href="getDownloadLink(file.name)" :download="file.name" viewer>
                {{ file.name }} ({{ formatBytes(file.size) }})
              </a>
            </li>
          </ul>
        </template>
        <template v-else>
          <p class="lead">当前没有可供下载的文件。</p>
        </template>
      </div>
    </div>
    <div v-show="activeIndex === '2'">
      <div class="jumbotron jumbotron-fluid">
        <div class="container">
          <div class="header">
            <div>
              <el-divider content-position="left">
                <el-tag class="mx-1" type="warning" round>
                  <h1 class="display-4">Copy Paste Tool</h1>
                </el-tag>
              </el-divider>
              <br>
              <p class="lead">这是一个方便快捷的文本传输效率工具，无字数限制，支持复制粘贴文本内容并实时同步，提供清空功能和复制到剪贴板。</p>
            </div>
            <img src="http://10.10.25.66/resource/erweima.png" class="erweima" v-if="!isMobile">
          </div>
        </div>
      </div>
      <el-input v-model="textarea" :autosize="{ minRows: 10, maxRows: 18 }" type="textarea" placeholder="点击输入..."
        @input="updateBackendTextarea" />
      <br><br>
      <el-button @click="copyToClipboard" type="primary">
        <el-icon><document-copy /></el-icon> 复制粘贴板
      </el-button>
      <el-button @click="clearTextarea" type="danger"><el-icon>
          <Delete />
        </el-icon>清空输入框</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

// 后端地址全局配置
axios.defaults.baseURL = 'http://10.10.243.201:5001';

export default {
  setup() {
    const serverFiles = ref([]);
    const selectedFiles = ref([]);
    const activeIndex = ref('1-1');
    const textarea = ref('');
    const isMobile = ref(false);
    const uploading = ref(false);
    const filesBadgeValue = ref('')

    // 后端地址
    const uploadAction = '/upload';

    const checkIsMobile = () => {
      const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      isMobile.value = isMobileDevice;
    };

    const handleSelect = (index) => {
      activeIndex.value = index.toString();
      if (activeIndex.value === '2') {
        fetchBackendTextarea();
      }
    };

    const fetchServerFiles = async () => {
      try {
        const response = await axios.get('/file_list');
        serverFiles.value = response.data.files;
        filesBadgeValue.value = response.data.files.length;
      } catch (error) {
        console.error('Error fetching server files:', error);
      }
    };

    const formatBytes = (bytes, decimals = 2) => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    };

    const updateRemainingTime = () => {
      setInterval(() => {
        serverFiles.value.forEach(file => {
          if (file.remainingTime > 0) {
            file.remainingTime -= 1;
          }
        });
      }, 1000);
    };

    const calculateProgress = (remainingTime) => {
      const totalSeconds = 5940;
      const progress = ((totalSeconds - remainingTime) / totalSeconds) * 100;
      return progress;
    };

    const getDownloadLink = (file) => {
      return `${axios.defaults.baseURL}/download/${file}`;
    };

    const handleFileChange = (event) => {
      selectedFiles.value = event.target.files;
    };

    const handleUpload = () => {
      uploading.value = true;
      const formData = new FormData();
      for (let i = 0; i < selectedFiles.value.length; i++) {
        formData.append('file', selectedFiles.value[i]);
      }
      axios.post('/upload', formData)
        .then(() => {
          uploading.value = false;
          fetchServerFiles();
        })
        .catch((error) => {
          uploading.value = false;
          ElMessage.error('上传文件时发生错误')
          console.error('上传文件时发生错误：', error);
        })
    };

    const copyToClipboard = () => {
      const input = document.createElement('input');
      input.value = textarea.value;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      ElMessage.success('Copied successfully!');
    };

    const clearTextarea = async () => {
      textarea.value = '';
      updateBackendTextarea()
      ElMessage.success('Cleared successfully!');
    };

    const updateBackendTextarea = async () => {
      try {
        await axios.post('/update_textarea', { content: textarea.value });
      } catch (error) {
        console.error('Error updating backend textarea:', error);
      }
    };

    const fetchBackendTextarea = async () => {
      try {
        const response = await axios.get('/get_textarea_content');
        textarea.value = response.data.content;
      } catch (error) {
        console.error('Error fetching backend textarea content:', error);
      }
    };

    onMounted(() => {
      fetchServerFiles();
      checkIsMobile();
      updateRemainingTime();
    });

    return {
      activeIndex,
      fetchServerFiles,
      handleSelect,
      serverFiles,
      formatBytes,
      getDownloadLink,
      textarea,
      copyToClipboard,
      updateBackendTextarea,
      fetchBackendTextarea,
      uploadAction,
      isMobile,
      handleFileChange,
      selectedFiles,
      uploading,
      handleUpload,
      clearTextarea,
      filesBadgeValue,
      calculateProgress
    };
  },
};
</script>

<style>
.container {
  width: 50%;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.erweima {
  width: 220px;
  height: auto;
}
</style>
