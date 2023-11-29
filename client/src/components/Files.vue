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

    <alert :message="message" v-if="showMessage"></alert>
    <input type="file" ref="fileInput" @change="handleFileChange" multiple />
    <div v-if="selectedFiles && selectedFiles.length > 0">
      <hr>
      <h5>Selected Files:</h5>
      <ul>
        <li v-for="(file, index) in selectedFiles" :key="index">
          {{ file.name }} ({{ formatBytes(file.size) }})
        </li>
      </ul>
    </div>
    <button type="button" class="btn btn-primary" @click="handleUpload"
      :disabled="!selectedFiles || selectedFiles.length === 0">
      Upload Files
    </button>
  </div>

  <div class="container">
    <br><br><br>
    <h4 style="text-align: right">File Download</h4>
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
import Alert from './Alert.vue';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  data() {
    return {
      serverFiles: [],
      selectedFiles: null,
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  mounted() {
    this.fetchServerFiles();
  },
  methods: {
    fetchServerFiles() {
      axios.get('http://10.10.243.201:5001/file_list')
        .then(response => {
          this.serverFiles = response.data.files;  // Use response.data.files
        })
        .catch(error => {
          console.error(error);
        });
    },
    handleFileChange(event) {
      this.selectedFiles = event.target.files;
    },
    handleUpload() {
      const formData = new FormData();
      for (let i = 0; i < this.selectedFiles.length; i++) {
        formData.append('file', this.selectedFiles[i]);
      }
      axios.post('http://10.10.243.201:5001/upload', formData)
        .then(() => {
          this.message = 'Files uploaded successfully!';
          this.showMessage = true;
          this.$nextTick(() => {
            this.fetchServerFiles();
          });
        })
        .catch((error) => {
          console.error(error);
          this.message = 'Error uploading files.';
          this.showMessage = true;
        });
    },
    formatBytes(bytes, decimals = 2) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    },
    getDownloadLink(file) {
      return `http://10.10.243.201:5001/download/${file}`;
    },
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
  /* Adjust the width as needed */
  height: auto;
}
</style>
