<template>
  <div class="container">
    <div
      style="flex-grow: 1; display: flex; justify-content: flex-end"
      v-if="!isMobile"
    >
      <el-descriptions style="width: auto" border>
        <el-descriptions-item>
          <template #label>
            <span style="font-size: 15px"> 已处理文件: </span>
          </template>
          <span :style="{ fontSize: '17px' }">
            {{ fileServiceCount }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <span style="font-size: 15px"> 已处理文本: </span>
          </template>
          <span :style="{ fontSize: '17px' }">
            {{ textServiceCount }}
          </span>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <div v-if="!isMobile">
      <el-badge value="new" class="item" style="margin-right: 800px">
        <el-button
          @click="navigateTo"
          size="large"
          type="primary"
          style="font-size: 18px"
        >
          <svg-icon iconName="iconpackage" />&nbsp;Package Viewer
        </el-button>
      </el-badge>
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
                <span style="font-size: 20px"> 🗂️ 文件 </span>
              </el-badge>
            </div>
            <div v-else>
              <span style="font-size: 20px"> 🗂️ 文件 </span>
            </div>
          </div>
        </template>
        <el-menu-item index="1-1" style="font-size: 20px">
          ⚙️组件方式
        </el-menu-item>
        <el-menu-item index="1-2" style="font-size: 20px"
          >非组件方式</el-menu-item
        >
      </el-sub-menu>
      <el-menu-item index="2" style="font-size: 20px">
        <el-badge class="item"> 🗒️ 文本 </el-badge>
      </el-menu-item>
    </el-menu>
    <br />
    <div v-show="activeIndex === '1-1'">
      <div
        class="container"
        :style="{ display: 'flex', flexDirection: isMobile ? 'column' : 'row' }"
      >
        <div style="width: 100%">
          <el-divider content-position="left">
            <el-tag class="mx-1" type="success" round>
              <h1 class="display-4">Upload Tool</h1>
            </el-tag>
          </el-divider>
          <br />
          <div class="mx-2" v-if="!isMobile">
            <h3 :class="'lead'">
              📑🔗你可以轻松地将文件上传到我们的服务器，并通过简单的点击下载你需要的文件。
            </h3>
            <h3 :class="'lead'">
              ⏳📊实时显示你上传文件的处理状态，包括剩余时间和处理进度，让你清楚地了解文件处理的情况。
            </h3>
            <h3 :class="'lead'">
              📱💻页面可以适应不同大小的设备，让你在任何设备上都能方便地使用文件共享功能。
            </h3>
          </div>
        </div>
        <div
          v-if="!isMobile"
          style="
            width: 20%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
          "
        >
          <img
            src="http://10.10.25.66/resource/erweima.png"
            class="erweima"
            style="height: 100%"
          />
        </div>
      </div>

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
      <br />
      <div class="container">
        <el-divider content-position="right">
          <el-tag class="mx-1" type="warning" round>
            <h4 class="display-6" style="text-align: right">File Download</h4>
          </el-tag>
        </el-divider>
        <template v-if="serverFiles.length > 0">
          <ul>
            <li v-for="(file, index) in serverFiles" :key="index">
              <div style="display: flex; align-items: center">
                <div style="flex: 100%">
                  <a href="#" @click.prevent="handleFileDownload(file.name)">
                    <div class="file-info-container">
                      <span
                        style="font-size: 17px; word-break: break-word"
                        :style="{ fontSize: isMobile ? '17px' : 'inherit' }"
                      >
                        {{ file.name }} ({{ formatBytes(file.size) }})
                      </span>
                    </div>
                  </a>
                </div>
                <div style="flex: 38%" v-if="!isMobile">
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
          <p class="lead">当前没有可供下载的文件。</p>
        </template>
      </div>
    </div>
    <div v-show="activeIndex === '1-2'">
      <div class="container" style="display: flex">
        <div style="width: 100%; display: flex; flex-direction: column">
          <el-divider content-position="left">
            <el-tag class="mx-1" type="success" round>
              <h1 class="display-4">Upload Tool</h1>
            </el-tag>
          </el-divider>
          <p />
          <div class="mx-2" v-if="!isMobile">
            <h3 :class="'lead'">
              📑🔗你可以轻松地将文件上传到我们的服务器，并通过简单的点击下载你需要的文件。
            </h3>
            <h3 :class="'lead'">
              ⏳📊实时显示你上传文件的处理状态，包括剩余时间和处理进度，让你清楚地了解文件处理的情况。
            </h3>
            <h3 :class="'lead'">
              📱💻页面可以适应不同大小的设备，让你在任何设备上都能方便地使用文件共享功能。
            </h3>
          </div>
        </div>
        <div
          style="
            width: 20%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
          "
        >
          <img
            src="http://10.10.25.66/resource/erweima.png"
            class="erweima"
            v-if="!isMobile"
            style="height: 100%"
          />
        </div>
      </div>
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
      <p />
      <button
        type="button"
        class="btn btn-primary upload-button"
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
      </button>
      <div class="container">
        <br />
        <el-divider content-position="right">
          <el-tag class="mx-1" type="warning" round>
            <h4 class="display-6" style="text-align: right">File Download</h4>
          </el-tag>
        </el-divider>
        <template v-if="serverFiles.length > 0">
          <ul>
            <li
              v-for="(file, index) in serverFiles"
              :key="index"
              style="width: 100%; word-wrap: break-word"
            >
              <a
                :href="getDownloadLink(file.name)"
                :download="file.name"
                viewer
              >
                <span :style="{ fontSize: isMobile ? '17px' : 'inherit' }">
                  {{ file.name }} ({{ formatBytes(file.size) }})
                </span>
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
      <div class="container" style="display: flex">
        <div style="width: 100%; display: flex; flex-direction: column">
          <el-divider content-position="left">
            <el-tag class="mx-1" type="success" round>
              <h1 class="display-4">Copy Paste Tool</h1>
            </el-tag>
          </el-divider>
          <p />
          <div class="mx-2" v-if="!isMobile">
            <h3 :class="'lead'">
              ✍️📝你可以在文本框中轻松地输入你想要传输的文本内容，界面简洁清晰，操作方便。
            </h3>
            <h3 :class="'lead'">
              📋✂️提供了一键复制文本内容到剪贴板的功能，让你可以轻松复制所需文本，提高了使用效率。
            </h3>
            <h3 :class="'lead'">
              🔄📑实时显示文本传输服务的处理次数和最新的文本内容，让你随时了解当前传输状态。
            </h3>
          </div>
        </div>
        <div
          style="
            width: 20%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
          "
        >
          <img
            src="http://10.10.25.66/resource/erweima.png"
            class="erweima"
            v-if="!isMobile"
            style="height: 100%"
          />
        </div>
      </div>
      <el-input
        v-model="textarea"
        :autosize="{ minRows: 10, maxRows: 18 }"
        type="textarea"
        placeholder="点击输入 或Ctrl + V / 选中右击 粘贴"
        @input="updateBackendTextarea"
      />
      <br /><br />
      <el-button @click="copyToClipboard" type="primary">
        <el-icon><document-copy /></el-icon>&nbsp;Copy
      </el-button>
      <el-button @click="clearTextarea" type="danger"
        ><el-icon> <Delete /> </el-icon>&nbsp;Clear</el-button
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
      "📂🔗你可以轻松地将文件上传到我们的服务器，并通过简单的点击下载你需要的文件。",
      "⏳📊实时显示你上传文件的处理状态，包括剩余时间和处理进度，让你清楚地了解文件处理的情况。",
      "📱💻页面可以适应不同大小的设备，让你在任何设备上都能方便地使用文件共享功能。",
    ]);
    const text_help = ref([
      "✍️📝你可以在文本框中轻松地输入你想要传输的文本内容，界面简洁清晰，操作方便。",
      "📋✂️提供了一键复制文本内容到剪贴板的功能，让你可以轻松复制所需文本，提高了使用效率。",
      "🔄📑实时显示文本传输服务的处理次数和最新的文本内容，让你随时了解当前传输状态。",
    ]);

    const router = useRouter();
    const navigateTo = () => {
      router.push("/package");
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
        fetchFileServiceCount(); // 更新服务次数
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
      ElMessage.success("Copied Success!");
      await axios.post("/increment_text_service_count");
      fetchTextServiceCount(); // 更新服务次数
    };

    const clearTextarea = async () => {
      textarea.value = "";
      updateBackendTextarea();
      ElMessage.success("Cleared Success!");
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
      navigateTo,
    };
  },
};
</script>

<style>
.container {
  width: 50%;
  margin: 0 auto;
}

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
  width: 200px;
  height: auto;
  transition: transform 0.3s ease;
}
.erweima:hover {
  transform: scale(1.05);
}
.erweima:hover {
  transform: scale(1.05);
}
</style>
