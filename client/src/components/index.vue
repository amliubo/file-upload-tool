<template>
  <div class="container">
    <div style="flex-grow: 1; display: flex; justify-content: flex-end;">
      <el-descriptions style="width: auto" border>
        <el-descriptions-item>
          <template #label>
            <span style="font-family: 'Comic Sans MS, cursive'; font-size: 15px;">
              已处理文件:
            </span>
          </template>
          <span :style="{ fontSize: '20px', color: '#28a745', fontFamily: 'Comic Sans MS, cursive' }">
            {{ fileServiceCount }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <span style="font-family: 'Comic Sans MS, cursive'; font-size: 15px;">
              已处理文本:
            </span>
          </template>
          <span :style="{ fontSize: '20px', color: '#28a745', fontFamily: 'Comic Sans MS, cursive' }">
            {{ textServiceCount }}
          </span>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-sub-menu index="1">
        <template #title>
          <div class="menu-title">
            <div v-if="filesBadgeValue > 0">
              <el-badge :value="filesBadgeValue" class="item" type="success">
                <span style="font-size: 17px;">
                  📂文件
                </span>
              </el-badge>
            </div>
            <div v-else>
              <span style="font-size: 17px;">
                📂文件
              </span>
            </div>
          </div>
        </template>
        <el-menu-item index="1-1" style="font-size: 17px;">
          ⚙️组件方式
        </el-menu-item>
        <el-menu-item index="1-2" style="font-size: 17px;">非组件方式</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="2" style="font-size: 17px;">
        <el-badge class="item">
          📄文本
        </el-badge>
      </el-menu-item>
    </el-menu>
    <br>
    <div v-show="activeIndex === '1-1'">
      <div class="container" style="display: flex;">
        <div style="width: 100%; display: flex; flex-direction: column;">
          <el-divider content-position="left">
            <el-tag class="mx-1" type="success" round>
              <h1 class="display-4">Upload Tool</h1>
            </el-tag>
          </el-divider>
          <br>
          <div class="mx-2">
            <el-carousel height="100px" direction="vertical" :autoplay="true">
              <el-carousel-item v-for="f_item in file_help" :key="f_item">
                <h3 :class="'lead'">{{ f_item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <div style="width: 20%; display: flex; justify-content: flex-end; align-items: center;">
          <img src="http://10.10.25.66/resource/erweima.png" class="erweima" v-if="!isMobile" style="height: 100%;">
        </div>
      </div>
      <el-upload class="upload-demo" drag action="http://10.10.243.201:5001/upload" multiple
        :on-success="fetchServerFiles">
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
                  <a href="#" @click.prevent="handleFileDownload(file.name)">
                    <span style="font-size: 18px;">{{ file.name }} ({{ formatBytes(file.size) }})</span>
                  </a>
                </div>
                <div style="flex: 38%;">
                  <el-progress status="exception" striped striped-flow :stroke-width="1"
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
      <div class="container" style="display: flex;">
        <div style="width: 100%; display: flex; flex-direction: column;">
          <el-divider content-position="left">
            <el-tag class="mx-1" type="success" round>
              <h1 class="display-4">Upload Tool</h1>
            </el-tag>
          </el-divider>
          <br>
          <div class="mx-2">
            <el-carousel height="100px" direction="vertical" :autoplay="true">
              <el-carousel-item v-for="item in file_help" :key="item">
                <h3 :class="'lead'">{{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <div style="width: 20%; display: flex; justify-content: flex-end; align-items: center;">
          <img src="http://10.10.25.66/resource/erweima.png" class="erweima" v-if="!isMobile" style="height: 100%;">
        </div>
      </div>
      <input type="file" ref="fileInput" @change="handleFileChange" multiple />
      <div v-if="selectedFiles && selectedFiles.length > 0">
        <hr>
        <h5>Selected Files:</h5>
        <ul>
          <li v-for="( file, index ) in selectedFiles " :key="index">
            {{ file.name }} ({{ formatBytes(file.size) }})
          </li>
        </ul>
      </div>
      <button type="button" class="btn btn-primary" @click="handleUpload"
        :disabled="!selectedFiles || selectedFiles.length === 0 || uploading">
        <span v-if="!uploading"><el-icon>
            <Upload />
          </el-icon>&nbsp;Upload</span>
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
            <li v-for="( file, index ) in serverFiles " :key="index">
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

      <div class="container" style="display: flex;">
        <div style="width: 100%; display: flex; flex-direction: column;">
          <el-divider content-position="left">
            <el-tag class="mx-1" type="success" round>
              <h1 class="display-4">Copy Paste Tool</h1>
            </el-tag>
          </el-divider>
          <br>
          <div class="mx-2">
            <el-carousel height="100px" direction="vertical" :autoplay="true">
              <el-carousel-item v-for="t_item in text_help" :key="t_item">
                <h3 :class="'lead'">{{ t_item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <div style="width: 20%; display: flex; justify-content: flex-end; align-items: center;">
          <img src="http://10.10.25.66/resource/erweima.png" class="erweima" v-if="!isMobile" style="height: 100%;">
        </div>
      </div>
      <el-input v-model="textarea" :autosize="{ minRows: 10, maxRows: 18 }" type="textarea"
        placeholder="点击输入 或Ctrl + V / 选中右击 粘贴" @input="updateBackendTextarea" />
      <br><br>
      <el-button @click="copyToClipboard" type="primary">
        <el-icon><document-copy /></el-icon>&nbsp;Copy
      </el-button>
      <el-button @click="clearTextarea" type="danger"><el-icon>
          <Delete />
        </el-icon>&nbsp;Clear</el-button>
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
    const filesBadgeValue = ref('');
    const fileServiceCount = ref(0);
    const textServiceCount = ref(0);

    const file_help = ref(['📣上传和下载文件：您可以轻松地将文件上传到我们的服务器，并通过简单的点击下载您需要的文件。📂🔗 Upload and download files: You can easily upload files to our server and download the files you need with simple clicks.',
      '📣实时处理状态：实时显示您上传文件的处理状态，包括剩余时间和处理进度，让您清楚地了解文件处理的情况。⏳📊 Real-time processing status: Display the processing status of your uploaded files in real time, including the remaining time and processing progress, so that you can clearly understand the status of file processing.',
      '📣适应不同设备：页面可以适应不同大小的设备，让您在任何设备上都能方便地使用文件共享功能。📱💻 Adapt to different devices: The page can adapt to devices of different sizes, allowing you to conveniently use the file sharing function on any device.']);
    const text_help = ref(['📣简单的文本输入：您可以在文本框中轻松地输入您想要传输的文本内容，界面简洁清晰，操作方便。✍️📝 Simple text input: You can easily enter the text content you want to transfer in the text box. The interface is simple and clear, and the operation is easy.',
      '📣快速复制粘贴：提供了一键复制文本内容到剪贴板的功能，让您可以轻松复制所需文本，提高了使用效率。📋✂️ Quick copy and paste: provides a one-click function to copy text content to the clipboard, allowing you to easily copy the required text and improve usage efficiency.',
      '📣实时同步文本：实时显示文本传输服务的处理次数和最新的文本内容，让您随时了解当前传输状态。🔄📑 Real-time synchronization text: Displays the processing times of the text transmission service and the latest text content in real time, allowing you to understand the current transmission status at any time.']);
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
        fetchTextServiceCount();
      } else if (activeIndex.value.startsWith('1')) {
        fetchFileServiceCount(); // 更新服务次数
      }
    };

    const fetchServerFiles = async () => {
      const response = await axios.get('/file_list');
      serverFiles.value = response.data.files;
      filesBadgeValue.value = response.data.files.length;
      fetchFileServiceCount(); // 更新服务次数
    };

    const fetchFileServiceCount = async () => {
      const response = await axios.get('/get_file_service_count');
      fileServiceCount.value = response.data.count;
    };

    const fetchTextServiceCount = async () => {
      const response = await axios.get('/get_text_service_count');
      textServiceCount.value = response.data.count;
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
          fetchFileServiceCount(); // 更新服务次数
        })
        .catch((error) => {
          uploading.value = false;
          ElMessage.error('上传文件时发生错误');
          console.error('上传文件时发生错误：', error);
        });
    };

    const copyToClipboard = async () => {
      const input = document.createElement('input');
      input.value = textarea.value;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      ElMessage.success('Copied Success!');
      await axios.post('/increment_text_service_count');
      fetchTextServiceCount();// 更新服务次数
    };

    const clearTextarea = async () => {
      textarea.value = '';
      updateBackendTextarea();
      ElMessage.success('Cleared Success!');
    };

    const updateBackendTextarea = async () => {
      await axios.post('/update_textarea', { content: textarea.value });
      fetchTextServiceCount(); // 更新服务次数
    };

    const fetchBackendTextarea = async () => {
      const response = await axios.get('/get_textarea_content');
      textarea.value = response.data.content;
    };

    const handleFileDownload = async (fileName) => {
      const downloadLink = getDownloadLink(fileName);
      window.location.href = downloadLink;
      setTimeout(() => {
        fetchFileServiceCount();
      }, 500);
    };

    onMounted(() => {
      fetchServerFiles();
      checkIsMobile();
      updateRemainingTime();
      fetchFileServiceCount();
      fetchTextServiceCount();
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
      fileServiceCount,
      textServiceCount,
      calculateProgress,
      handleFileDownload,
      file_help,
      text_help,
    };
  },
};
</script>

<style>
.container {
  width: 50%;
  margin: 0 auto;
}

.erweima {
  width: 200px;
  height: auto;
}
</style>
