<template>
  <div class="app">
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <el-badge value="hot" class="item">
        <el-button
          @click="navigateTo"
          size="large"
          type="primary"
          style="font-size: 18px"
        >
          <svg-icon iconName="iconxiaoshuai" />&nbsp;文件 / 文本共享
        </el-button>
      </el-badge>
      <el-divider
        content-position="right"
        style="flex-grow: 1; margin-left: 20px"
      >
        <el-tag type="success" round>
          <p style="font-size: 52px">Package Viewer</p>
        </el-tag>
      </el-divider>
    </div>
    <p :class="'lead'" style="font-size: 31px">
      <svg-icon iconName="iconhuojian" /><svg-icon iconName="iconhuojian" />
      我们可以帮助你轻松导航到最新 Package，并提供多种安装方式供你使用。
    </p>
    <el-input
      v-model="search"
      placeholder="Type to search ( support Branches、Channel、Build Plan、Network )"
      class="zoom-input"
      style="margin-bottom: 20px; height: 44px"
    />
    <el-table
      v-loading="loading"
      :data="filteredData"
      stripe
      style="width: 100%; font-size: 18px; font-family: Arial, sans-serif"
      :element-loading-text="'加载中...'"
    >
      <el-table-column prop="branch" label="Branches" width="320" />
      <el-table-column prop="channel" label="Channel" width="180" />
      <el-table-column prop="build_plan" label="Build Plan" width="180" />
      <el-table-column prop="network" label="Network" width="150" />
      <el-table-column prop="build_time" label="Build Time" width="160" />
      <el-table-column prop="operate" label="Operate">
        <template v-slot="scope">
          <div class="operate-column">
            <div class="operation-item">
              <svg-icon iconName="iconxiazai" class="icon-style" />
              <el-link
                :type="scope.row.package_url ? 'primary' : 'info'"
                :disabled="!scope.row.package_url"
                @click="handleDownload(scope.row.package_url)"
                target="_blank"
                class="link-style"
              >
                {{
                  scope.row.package_url &&
                  scope.row.package_url.endsWith(".apk")
                    ? "下载apk"
                    : "下载ipa"
                }}
              </el-link>
            </div>
            <div class="operation-item">
              <el-popover placement="right" width="200" trigger="hover">
                <template v-slot:reference>
                  <span class="link-style">
                    <svg-icon iconName="iconiconfontscan" class="icon-style" />
                    <el-link
                      :type="scope.row.png_url ? 'danger' : 'info'"
                      :disabled="!scope.row.png_url"
                      class="link-style"
                    >
                      二维码
                    </el-link>
                  </span>
                </template>
                <img
                  v-if="scope.row.png_url"
                  :src="scope.row.png_url"
                  class="qr-code"
                />
                <span v-else>❌无二维码</span>
              </el-popover>
            </div>
            <div class="operation-item">
              <svg-icon iconName="iconjenkins" class="icon-style" />
              <el-link
                type="success"
                @click="handleDownload(scope.row.jenkins_url)"
                target="_blank"
                class="link-style"
              >
                Jenkins Detail
              </el-link>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import SvgIcon from "@/components/SvgIcon.vue";
export default {
  setup() {
    const loading = ref(true);
    const tableData = ref([]);
    const search = ref("");
    const fetchServerFiles = async (project) => {
      try {
        const response = await axios.get("/get_build_data");
        tableData.value = Array.isArray(response.data)
          ? response.data
          : [response.data];
      } finally {
        loading.value = false;
      }
    };
    const router = useRouter();
    const navigateTo = () => {
      router.push("/");
    };
    const handleDownload = (url) => {
      window.open(url, "_blank");
    };

    const filteredData = computed(() => {
      if (!search.value) {
        return tableData.value;
      }
      return tableData.value.filter((item) => {
        return (
          item.branch.toLowerCase().includes(search.value.toLowerCase()) ||
          item.channel.toLowerCase().includes(search.value.toLowerCase()) ||
          item.build_plan.toLowerCase().includes(search.value.toLowerCase()) ||
          item.network.toLowerCase().includes(search.value.toLowerCase())
        );
      });
    });

    onMounted(() => {
      fetchServerFiles();
    });

    return {
      SvgIcon,
      loading,
      tableData,
      search,
      filteredData,
      navigateTo,
      handleDownload,
    };
  },
};
</script>

<style scoped>
.app {
  width: 66%;
  margin: 0 auto;
}

::v-deep .el-table th {
  color: #ff7f7f;
}

::v-deep .el-table th .cell {
  background-color: #f0f0f0;
}

.zoom-input {
  transition: transform 0.3s ease;
}

.zoom-input:hover {
  transform: scale(1.05);
}

.icon-style {
  font-size: 18px;
  margin-right: 5px;
}

.description {
  text-align: center;
  font-size: 1rem;
  margin: 20px 0;
  color: #3b3b3b;
}

.operation-item {
  display: inline-flex;
  flex-wrap: wrap;
  width: 46%;
  /* margin-bottom: 2px; */
}

.operation-column {
  display: flex;
  flex-wrap: wrap;
}

.qr-code {
  width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}
</style>
