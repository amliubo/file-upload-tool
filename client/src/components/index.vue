<template>
  <div class="app">
    <div
      style="flex-grow: 1; display: flex; justify-content: flex-end"
      v-if="!isMobile"
    >
      <div class="container">
        <el-badge value="new" class="item">
          <el-button round @click="navigateTo"
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
          🔄组件方式
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
      <p></p>
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
      <p></p>
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
        style="height: 27px"
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
      <p></p>
      <el-card
        shadow="never"
        v-for="(card, index) in cards"
        :key="index"
        class="custom-card"
      >
        <div class="card-title" v-if="card.card_title">
          <el-badge type="info" :value="card.card_title" />
        </div>
        <div class="card-header">
          <el-badge type="warning" :value="'# ' + card.card_id" />
        </div>
        <div class="card-content">
          {{ card.content }}
        </div>
        <div class="card-buttons">
          <el-button
            type="success"
            @click="copyToClipboard(card.content)"
            icon="CopyDocument"
            round
            plain
            size="small"
            style="margin-right: -5px; height: 20px"
            >Cp
          </el-button>
          <el-button
            type="danger"
            @click="deleteCard(index)"
            icon="Delete"
            round
            plain
            size="small"
            style="height: 20px"
            >Del
          </el-button>
        </div>
      </el-card>
      <el-input
        v-model="textarea"
        :autosize="{ minRows: 8, maxRows: 16 }"
        type="textarea"
        placeholder="Ctrl + c / v"
        @input="updateBackendTextarea"
        class="custom-input"
      />
      <div style="margin-top: 5px">
        <el-button
          @click="addCard"
          type="primary"
          style="margin-right: -5px; width: 70px; height: 27px"
        >
          <el-icon><Open /></el-icon>&nbsp;Ding
        </el-button>
        <el-button
          @click="copyToClipboard()"
          type="success"
          style="margin-right: -5px; width: 70px; height: 27px"
          ><el-icon><CopyDocument /></el-icon>&nbsp;Copy</el-button
        >
        <el-button
          type="danger"
          @click="clearTextarea"
          style="width: 70px; height: 27px"
        >
          <el-icon><Delete /></el-icon>&nbsp;Clear
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { checkIsMobile, showNotification } from "../utils/utils";
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

export default {
  setup() {
    const isMobile = ref(false);
    const uploadAction = import.meta.env.VITE_UPLOAD_URL;
    const serverFiles = ref([]);
    const selectedFiles = ref([]);
    const activeIndex = ref("1-1");
    const textarea = ref("");
    const cards = ref([]);
    const uploading = ref(false);
    const filesBadgeValue = ref("");
    const fileServiceCount = ref(0);
    const textServiceCount = ref(0);
    const file_help = ref([
      "✈️ 简单上传文件并轻松下载。⌛ 实时显示上传状态，了解进度。",
      "🔄 支持组件和非组件方式，兼容全系统版本。🖥️ 页面自适应，随时随地使用文件共享。",
    ]);
    const text_help = ref([
      "🚀 输入文本轻松传输，界面简洁，操作方便。📝 一键复制文本到剪贴板，提升效率。",
      "⌛ 实时显示传输次数与最新内容，随时了解状态。✨ 新增'Ding'功能，轻松管理文本信息。",
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
      fetchFileServiceCount();
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
      axios.post("/upload", formData).then(() => {
        uploading.value = false;
        fetchServerFiles();
        fetchFileServiceCount();
      });
    };

    const copyToClipboard = async (content = null) => {
      if (!content) {
        if (textarea.value.trim().length !== 0) {
          content = textarea.value;
        } else {
          return;
        }
      }
      const tempTextarea = document.createElement("textarea");
      tempTextarea.value = content;
      document.body.appendChild(tempTextarea);
      tempTextarea.select();
      document.execCommand("copy");
      document.body.removeChild(tempTextarea);
      await axios.post("/increment_text_service_count");
      fetchTextServiceCount();
      showNotification("内容复制粘贴板！", isMobile.value, "msg");
    };

    const clearTextarea = async () => {
      if (textarea.value.trim().length !== 0) {
        textarea.value = "";
        updateBackendTextarea();
        showNotification("内容清空！", isMobile.value, "msg");
      }
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

    const fetchCards = async () => {
      const response = await axios.get("/get_card_contents");
      cards.value = response.data.cards || [];
    };

    const addCard = async () => {
      if (textarea.value.trim()) {
        const response = await axios.post("/save_card_content", {
          content: textarea.value,
        });
        const { card_id, content, card_title } = response.data;
        cards.value.unshift({ content, card_id, card_title });
        textarea.value = "";
        showNotification("Ding! 内容置顶！", isMobile.value, "msg");
      }
    };

    const deleteCard = async (index) => {
      await axios.post("/delete_card_content", { index: index });
      fetchCards();
      showNotification("删除成功！", isMobile.value, "msg");
    };

    onMounted(() => {
      isMobile.value = checkIsMobile();
      const safariVersion = detectSafariVersion();
      if (safariVersion !== null && safariVersion < 14) {
        activeIndex.value = "1-2";
      } else {
        activeIndex.value = "1-1";
      }
      fetchCards();
      fetchServerFiles();
      updateRemainingTime();
      fetchFileServiceCount();
      fetchTextServiceCount();
    });

    return {
      isMobile,
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
      cards,
      addCard,
      deleteCard,
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
  top: 150px;
  width: 150px;
  position: absolute;
  right: 26.5%;
}

.erweima:hover {
  transform: scale(1.05);
}
.erweima:hover {
  transform: scale(1.05);
}

.custom-input {
  transition: box-shadow 0.3s ease-in-out;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.custom-card {
  position: relative;
  margin-bottom: 10px;
}

.card-title {
  position: absolute;
  top: 1px;
  left: 10px;
}

.card-header {
  position: absolute;
  top: 2px;
  right: 2px;
}

.card-content {
  margin: -4px;
  font-size: 14px;
  font-weight: 200;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 2;
}
.card-buttons {
  position: absolute;
  right: 10px;
  display: flex;
}

.msg {
  height: 20px;
}
</style>
