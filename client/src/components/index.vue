<template>
  <div class="container">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1" style="font-size: 16px;">文件传输</el-menu-item>
      <el-menu-item index="2" style="font-size: 16px;">文本传输</el-menu-item>
    </el-menu>
    <br>
    <div v-if="activeIndex === '1'">
      <div class="jumbotron jumbotron-fluid">
        <div class="container">
          <div class="header">
            <div>
              <h1 class="display-4">Upload Tool</h1>
              <p class="lead">This is a lightweight and fast file transfer efficiency tool with no size limit.</p>
            </div>
            <!-- Logo -->
            <img src="@/assets/logo.png" alt="Download Icon" class="logo">
          </div>
        </div>
      </div>
      <hr><br>
      <el-upload class="upload-demo" drag action="http://10.10.20.24:5001/upload" multiple :on-success="fetchServerFiles">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
      </el-upload>
      <div class="container">
        <br>
        <h4 class="display-6" style="text-align: right">File Download</h4>
        <hr><br>
        <template v-if="serverFiles.length > 0">
          <ul>
            <li v-for="(file, index) in serverFiles" :key="index">
              <a :href="getDownloadLink(file.name)" :download="file.name" viewer>
                {{ file.name }} ({{ formatBytes(file.size) }})
              </a>
            </li>
          </ul>
        </template>
        <template v-else>
          <p>当前没有可供下载的文件。</p>
        </template>
      </div>
    </div>
    <div v-else-if="activeIndex === '2'">
      <div class="jumbotron jumbotron-fluid">
        <div class="container">
          <div class="header">
            <div>
              <h1 class="display-4">Text Transfer Tool</h1>
              <p class="lead">This is a lightweight and convenient text transmission efficiency tool with no word limit.
              </p>
            </div>
            <!-- Logo -->
            <img src="@/assets/logo.png" alt="Download Icon" class="logo">
          </div>
        </div>
      </div>
      <hr><br>
      <el-input v-model="textarea" :autosize="{ minRows: 12, maxRows: 24 }" type="textarea" placeholder="Please input..."
        @input="updateBackendTextarea" />
      <br><br>
      <el-button @click="copyToClipboard" type="primary">
        <el-icon><document-copy /></el-icon>
        Copy to Clipboard
      </el-button>
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
    const activeIndex = ref('1');
    const textarea = ref('');

    // 后端地址
    const uploadAction = '/upload';

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

    const getDownloadLink = (file) => {
      return `/download/${file}`;
    };

    const copyToClipboard = () => {
      const input = document.createElement('input');
      input.value = textarea.value;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      ElMessage.success('Text successfully copied to clipboard');
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

.logo {
  width: 280px;
  height: auto;
}
</style>
