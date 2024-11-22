<template>
  <div class="app">
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <el-badge value="hot" class="item">
        <el-button plain @click="navigateTo"
          ><svg-icon iconName="icongongxiangzhongxin" />&nbsp;Upload
          Tool</el-button
        >
      </el-badge>
      <el-tag type="success" round>
        <!-- <p
          style="
            font-size: 34px;
            font-weight: 300;
            text-align: right;
            font-style: italic;
            letter-spacing: 2px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
          "
        >
          Package Tool
        </p> -->
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
          Package Tool
        </p>
      </el-tag>
    </div>
    <p></p>
    <p style="font-size: 20px; font-weight: 300">
      我们可以帮助你轻易获取多渠道最新Package，并提供多种操作供你使用。
    </p>
    <el-input
      v-model="search"
      placeholder="搜索内容 ( 支持： Branches、Channel、Build Plan、Network )"
      class="zoom-input"
      style="margin-bottom: 20px; height: 38px"
    />
    <custom-loading :loading="loading" />
    <el-table
      v-if="!loading"
      :data="filteredData"
      stripe
      style="width: 100%; font-size: 16px"
    >
      <el-table-column prop="os" label="OS" width="60" align="center">
        <template v-slot="scope">
          <div class="icon-logo">
            <svg-icon v-if="scope.row.os === '.apk'" iconName="iconanzhuo" />
            <svg-icon v-else-if="scope.row.os === '.ipa'" iconName="iconiOS" />
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="branch"
        label="Branche"
        align="center"
        width="90"
      />
      <el-table-column
        prop="channel"
        label="Channel"
        align="center"
        width="90"
      />
      <el-table-column
        prop="build_plan"
        label="Build Plan"
        align="center"
        width="110"
      />
      <el-table-column
        prop="network"
        label="Network"
        align="center"
        width="100"
      />
      <el-table-column
        prop="build_time"
        label="Build Time"
        align="center"
        width="140"
      />
      <el-table-column prop="operate" label="Operate">
        <template v-slot="scope">
          <div class="operation-row">
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
                <img :src="scope.row.png_url" class="qr-code" />
              </el-popover>
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
    const fetchServerFiles = async () => {
      try {
        const response = await axios.get("/get_build_data");
        tableData.value = Array.isArray(response.data)
          ? response.data
          : [response.data];
        console.log(tableData.value);
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
          item.branch.includes(search.value.toLowerCase()) ||
          item.channel.includes(search.value.toLowerCase()) ||
          item.build_plan.includes(search.value.toLowerCase()) ||
          item.network.includes(search.value.toLowerCase())
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
  width: 50%;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

::v-deep .el-table th {
  color: #ff7f7f;
}

::v-deep .el-table th .cell {
  background-color: #f0f0f0;
}

.zoom-input:hover {
  transform: scale(1.05);
}

.zoom-input {
  transition: transform 0.3s ease;
  border-radius: 10px;
}

.zoom-input:hover {
  transform: scale(1.03);
}

.icon-logo {
  font-size: 42px;
  display: flex;
}

.icon-style {
  font-size: 20px;
  margin-right: 4px;
  transition: color 0.3s ease;
}

.operation-item {
  display: inline-flex;
  align-items: center;
  margin-right: 10px;
}

.qr-code {
  width: 100%;
  margin: 0 auto;
}

.link-style {
  font-size: 16px;
}

.el-table-column {
  padding: 10px 0;
}
</style>
