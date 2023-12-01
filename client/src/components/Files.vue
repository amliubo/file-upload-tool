<template>
  <div class="container">
    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <!-- Flex container for header -->
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
    <el-upload class="upload-demo" drag action="http://10.10.234.201:5001/upload" multiple :on-success="fetchServerFiles">
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
    </el-upload>
  </div>
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
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  setup() {
    const serverFiles = ref([]);

    const fetchServerFiles = () => {
      axios.get('http://10.10.243.201:5001/file_list')
        .then(response => {
          serverFiles.value = response.data.files;
        })
        .catch(error => {
          console.error(error);
        });
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
      return `http://10.10.20.243.201:5001/download/${file}`;
    };

    onMounted(() => {
      fetchServerFiles();
    });

    return {
      serverFiles,
      formatBytes,
      getDownloadLink,
      fetchServerFiles
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
  width: 240px;
  height: auto;
}
</style>
