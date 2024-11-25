<template>
  <div class="app">
    <div
      style="flex-grow: 1; display: flex; justify-content: flex-end"
      v-if="!isMobile"
    >
      <div class="container">
        <el-badge value="new" class="item">
          <el-button plain @click="navigateTo"
            ><svg-icon iconName="iconquanqudao" />&nbsp;Package Tool</el-button
          >
        </el-badge>
        <el-descriptions>
          <el-descriptions-item>
            <template #label>
              <span
                style="
                  text-align: right;
                  font-style: italic;
                  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                "
                >已处理文件：{{ fileServiceCount }}</span
              >
              &nbsp;
              <span
                style="
                  text-align: right;
                  font-style: italic;
                  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                "
                >已处理文本：{{ textServiceCount }}</span
              >
            </template>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-sub-menu index="1">
        <template #title>
          <div class="menu-title">
            <div v-if="filesBadgeValue > 0">
              <el-badge :value="filesBadgeValue" class="item" type="success">
                <span style="font-size: 18px">🗂️ 文件</span>
              </el-badge>
            </div>
            <div v-else>
              <span style="font-size: 18px">🗂️ 文件</span>
            </div>
          </div>
        </template>
        <el-menu-item index="1-1" style="font-size: 17px">
          ⚙️组件方式
        </el-menu-item>
        <el-menu-item index="1-2" style="font-size: 17px"
          >非组件方式</el-menu-item
        >
      </el-sub-menu>
      <el-menu-item index="2">
        <el-badge style="font-size: 18px">🗒️ 文本</el-badge>
      </el-menu-item>
    </el-menu>
    <br />
    <div
      v-if="activeIndex === '1-1' || activeIndex === '1-2'"
      :style="{ display: 'flex', flexDirection: isMobile ? 'column' : 'row' }"
    >
      <div>
        <el-tag round>
          <p
            style="
              font-size: 34px;
              font-weight: 300;
              text-align: right;
              font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
              font-style: italic;
              transform: skew(-5deg, -2deg);
              letter-spacing: 1.5px;
              line-height: 1.2;
            "
          >
            Upload Tool
          </p>
        </el-tag>
        <p></p>
        <div v-if="!isMobile" style="font-size: 18px; font-weight: 300">
          <p
            v-for="(item, index) in file_help"
            :key="index"
            style="margin-bottom: 1px"
          >
            {{ item }}
          </p>
        </div>
      </div>
      <div v-if="!isMobile">
        <img :src="erwm" class="erweima" />
      </div>
    </div>

    <div v-if="activeIndex === '1-1'">
      <el-upload
        class="upload-demo"
        drag
        :action="uploadAction"
        multiple
        @success="fetchServerFiles"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">将文件拖放到此处或<em>单击上传</em></div>
      </el-upload>
    </div>
    <div v-else-if="activeIndex === '1-2'">
      <input type="file" ref="fileInput" @change="handleFileChange" multiple />
      <div v-if="selectedFiles && selectedFiles.length > 0">
        <hr />
        <h5>Selected Files:</h5>
        <ul>
          <li v-for="(file, index) in selectedFiles" :key="index">
            {{ file.name }} ({{ formatBytes(file.size) }})
          </li>
        </ul>
      </div>
      <el-button
        type="primary"
        @click="handleUpload"
        :disabled="!selectedFiles || selectedFiles.length === 0 || uploading"
      >
        <span v-if="!uploading">
          <el-icon>
            <Upload />
          </el-icon>
          Upload
        </span>
        <span v-else>
          <i class="loading-icon el-icon-loading"></i>
          Loading...
        </span>
      </el-button>
    </div>
    <div v-show="activeIndex === '1-1' || activeIndex === '1-2'">
      <el-divider content-position="right">
        <el-tag round>
          <p
            style="
              font-size: 20px;
              font-weight: 300;
              text-align: right;
              font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
              font-style: italic;
              transform: skew(-5deg, -2deg);
              letter-spacing: 1.5px;
              line-height: 1.2;
            "
          >
            File Download
          </p>
        </el-tag>
      </el-divider>
      <template v-if="serverFiles.length > 0">
        <ul>
          <li v-for="(file, index) in serverFiles" :key="index">
            <div style="display: flex; align-items: center">
              <div style="flex: 100%">
                <a href="#" @click.prevent="handleFileDownload(file.name)">
                  <div class="file-info-container">
                    <span style="font-size: 14px">
                      {{ file.name }} ({{ formatBytes(file.size) }})
                    </span>
                  </div>
                </a>
              </div>
              <div style="flex: 50%" v-if="!isMobile">
                <el-progress
                  status="exception"
                  striped
                  striped-flow
                  :stroke-width="1"
                  :percentage="calculateProgress(file.remainingTime)"
                  color="red"
                />
              </div>
            </div>
          </li>
        </ul>
      </template>
      <template v-else>
        <p style="font-size: 18px; font-weight: 300">
          当前没有可供下载的文件。
        </p>
      </template>
    </div>
    <div v-show="activeIndex === '2'">
      <div
        :style="{ display: 'flex', flexDirection: isMobile ? 'column' : 'row' }"
      >
        <div>
          <el-tag round>
            <p
              style="
                font-size: 34px;
                font-weight: 300;
                text-align: right;
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
                font-style: italic;
                transform: skew(-5deg, -2deg);
                letter-spacing: 1.5px;
                line-height: 1.2;
              "
            >
              Copy Paste Tool
            </p>
          </el-tag>
          <p></p>
          <div v-if="!isMobile" style="font-size: 18px; font-weight: 300">
            <p
              v-for="(item, index) in text_help"
              :key="index"
              style="margin-bottom: 1px"
            >
              {{ item }}
            </p>
          </div>
        </div>
        <div v-if="!isMobile">
          <img :src="erwm" class="erweima" />
        </div>
      </div>
      <el-input
        v-model="textarea"
        :autosize="{ minRows: 10, maxRows: 18 }"
        type="textarea"
        placeholder="Ctrl + c / v"
        @input="updateBackendTextarea"
      />
      <p></p>
      <el-button @click="copyToClipboard" type="primary">
        <el-icon><document-copy /></el-icon>&nbsp;复制
      </el-button>
      <el-button @click="clearTextarea" type="danger"
        ><el-icon> <Delete /> </el-icon>&nbsp;清空</el-button
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

export default {
  setup() {
    const uploadAction = import.meta.env.VITE_UPLOAD_URL;
    const serverFiles = ref([]);
    const selectedFiles = ref([]);
    const activeIndex = ref("1-1");
    const textarea = ref("");
    const isMobile = ref(false);
    const uploading = ref(false);
    const filesBadgeValue = ref("");
    const fileServiceCount = ref(0);
    const textServiceCount = ref(0);
    const file_help = ref([
      "✈️你可以轻松地将文件上传到我们的服务器，并通过简单的点击下载你需要的文件。",
      "⌛实时显示你上传文件的处理状态，包括剩余时间让你清楚了解文件处理的情况。",
      "🖥️页面可以适应不同大小的设备，让你在任何设备上都能方便地使用文件共享功能。",
    ]);
    const text_help = ref([
      "🚀你可以在文本框中轻松地输入你想要传输的文本内容，界面简洁清晰，操作方便。",
      "📝提供一键复制文本内容到剪贴板的功能，让你可以轻松复制所需文本，提高了使用效率。",
      "⌛实时显示文本传输服务的处理次数和最新的文本内容，让你随时了解当前传输状态。",
    ]);
    const erwm = ref("http://10.10.25.66/resource/erweima.png");
    const router = useRouter();
    const navigateTo = () => {
      router.push("/pkg");
    };

    const detectSafariVersion = () => {
      const userAgent = navigator.userAgent;
      const safariVersionMatch = userAgent.match(/Version\/(\d+)/);
      if (safariVersionMatch) {
        const version = parseInt(safariVersionMatch[1], 10);
        return version;
      }
      return null;
    };
    const checkIsMobile = () => {
      const isMobileDevice =
        /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
          navigator.userAgent
        );
      isMobile.value = isMobileDevice;
    };

    const handleSelect = (index) => {
      activeIndex.value = index.toString();
      if (activeIndex.value === "2") {
        fetchBackendTextarea();
        fetchTextServiceCount();
      } else if (activeIndex.value.startsWith("1")) {
        fetchFileServiceCount();
      }
    };

    const fetchServerFiles = async () => {
      const response = await axios.get("/file_list");
      serverFiles.value = response.data.files;
      filesBadgeValue.value = response.data.files.length;
      fetchFileServiceCount(); // 更新服务次数
    };

    const fetchFileServiceCount = async () => {
      const response = await axios.get("/get_file_service_count");
      fileServiceCount.value = response.data.count;
    };

    const fetchTextServiceCount = async () => {
      const response = await axios.get("/get_text_service_count");
      textServiceCount.value = response.data.count;
    };

    const formatBytes = (bytes, decimals = 2) => {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    };

    const updateRemainingTime = () => {
      setInterval(() => {
        serverFiles.value.forEach((file) => {
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
        formData.append("file", selectedFiles.value[i]);
      }
      axios
        .post("/upload", formData)
        .then(() => {
          uploading.value = false;
          fetchServerFiles();
          fetchFileServiceCount();
        })
        .catch((error) => {
          uploading.value = false;
          ElMessage.error("上传文件时发生错误");
          console.error("上传文件时发生错误：", error);
        });
    };

    const copyToClipboard = async () => {
      const input = document.createElement("input");
      input.value = textarea.value;
      document.body.appendChild(input);
      input.select();
      document.execCommand("copy");
      document.body.removeChild(input);
      ElMessage.success("复制成功！");
      await axios.post("/increment_text_service_count");
      fetchTextServiceCount(); // 更新服务次数
    };

    const clearTextarea = async () => {
      textarea.value = "";
      updateBackendTextarea();
      ElMessage.success("清理成功！");
    };

    const updateBackendTextarea = async () => {
      await axios.post("/update_textarea", { content: textarea.value });
      fetchTextServiceCount();
    };

    const fetchBackendTextarea = async () => {
      const response = await axios.get("/get_textarea_content");
      textarea.value = response.data.content;
    };

    const handleFileDownload = async (fileName) => {
      const downloadLink = getDownloadLink(fileName);
      const link = document.createElement("a");
      link.href = downloadLink;
      link.download = fileName;
      link.click();
      setTimeout(() => {
        fetchFileServiceCount();
      }, 500);
    };

    onMounted(() => {
      const safariVersion = detectSafariVersion();
      if (safariVersion !== null && safariVersion < 14) {
        activeIndex.value = "1-2";
      } else {
        activeIndex.value = "1-1";
      }
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
      erwm,
      navigateTo,
    };
  },
};
</script>

<style>
.app {
  width: 100%;
  margin: 0 auto;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (min-width: 768px) {
  .app {
    width: 50%;
  }
}

/* 统计部分 */
.container {
  display: flex;
  justify-content: space-between;
}
/* 上传组件 */

.file-info-container {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.file-info-container:hover {
  transform: translateY(-8px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}
.fade-in {
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}
.fade-in.visible {
  opacity: 1;
}
.erweima {
  width: 150px;
  transition: transform 0.3s ease;
}
.erweima:hover {
  transform: scale(1.05);
}
.erweima:hover {
  transform: scale(1.05);
}
</style>
