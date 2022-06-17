<template>
  <div class="main-container">
    <div class="page-header">Article Management</div>
    <div class="page-content">
      <div style="display: flex; margin-bottom: 30px;">
        <el-input style="width: 200px;" v-model="aid" placeholder="aid"></el-input>
        <el-button style="width: 100px; margin-left: 70px;" type="primary" @click="getArticle">Go</el-button>
      </div>
      <el-table
        :data="tableData"
        style="width: 95%"
        height="500"
        :border="true"
      >
        <el-table-column label="AID" width="70">
          <template slot-scope="scope">
            <span>{{ scope.row.aid }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Title">
          <template slot-scope="scope">
            <el-tooltip
              class="item"
              effect="dark"
              :content="scope.row.abstract"
              placement="top-start"
            >
              <span style="font-weight: bold; font-style: italic;">{{
                scope.row.title
              }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="Author">
          <template slot-scope="scope">
            <span>{{ scope.row.authors }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Category">
          <template slot-scope="scope">
            <span v-if="scope.row.category === 'science'" class="label-green">
              {{ scope.row.category }}
            </span>
            <span
              v-else-if="scope.row.category === 'technology'"
              class="label-blue"
            >
              {{ scope.row.category }}
            </span>
            <span v-else class="label-yellow">
              {{ scope.row.category }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="Tags">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.articleTags }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Language">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.language }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="180">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="getArticleDetail(scope.$index, scope.row)"
            >
              Details
            </el-button>
            <el-button
              size="mini"
              @click="getArticleStatus(scope.$index, scope.row)"
            >
              Status
            </el-button>
            <!-- <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button
            > -->
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      :title="selectedArticle.title"
      :visible.sync="dialogDetail"
      width="70%"
    >
      <div>{{ selectedArticleDetail.content }}</div>
      <div style="display: flex; margin-top: 30px;">
        <div v-for="img in selectedArticleDetail.image" :key="img">
          <el-image
            style="width: 200px; height: 200px"
            :src="$baseURL + img"
            fit="scale-down"
          ></el-image>
        </div>
      </div>
        <video
          v-if="selectedArticleDetail.video !== undefined && selectedArticleDetail.video !== ''"
          style="margin-top: 30px;"
          autoplay
          controls
          width="100%"
          height="500"
          id="videoElement"
        ></video>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogDetail = false">OK</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="selectedArticle.title"
      :visible.sync="dialogStatus"
      width="30%"
    >
      <div style="margin-left: 30px;">
        <el-table
          :data="selectedArticleStatus"
          :show-header="false"
          :cell-class-name="tableCellClassName"
          :border="true">
          <el-table-column label="Type">
            <template slot-scope="scope">
              <span>{{ scope.row.type }}</span>
            </template>
          </el-table-column>
          <el-table-column label="Num">
            <template slot-scope="scope">
              <span>{{ scope.row.num }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogStatus = false">OK</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import qs from "qs";
import flvjs from "flv.js";

export default {
  name: "ArticleManagement",
  data() {
    return {
      dialogDetail: false,
      selectedArticle: {},
      selectedArticleDetail: {},
      aid: '1',
      tableData: [],
      dialogStatus: false,
      selectedArticleStatus: []
    };
  },
  created() {
    this.getArticle();
  },
  methods: {
    createVideo() {
      if (flvjs.isSupported()) {
        var videoElement = document.getElementById("videoElement");
        var flvPlayer = flvjs.createPlayer({
          type: "flv",
          url: this.$baseURL + this.selectedArticleDetail.video //你的url地址
        });
        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
        flvPlayer.play();
      }
    },
    tableCellClassName({ row, column, rowIndex, columnIndex }) {
      if (rowIndex === 0 && columnIndex === 0) {
        return "label-green";
      } else if (rowIndex === 1 && columnIndex === 0) {
        return "label-blue";
      } else if (rowIndex === 2 && columnIndex === 0) {
        return "label-yellow";
      } else if (rowIndex === 3 && columnIndex === 0) {
        return "label-sliver";
      }
      return "";
    },
    getArticle() {
      // period: day/week/month, date: string, num: int
      let data = {
        aid: this.aid
      };
      this.$axios
        .get("/api/article?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get article(s)", res);
            this.tableData = res.data.data.article;
            this.$message.success("Success: get article(s)");
          } else {
            console.log("Error: get article(s)", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get article(s)", error);
          this.$message.error("Error: get article(s)", error);
        });
    },
    getArticleDetail(index, row) {
      this.selectedArticle = this.tableData[index];
      this.dialogDetail = true;
      let data = {
        aid: this.selectedArticle.aid % 1000
      };
      this.$axios
        .get("/api/article/detail?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get article detail", res);
            this.selectedArticleDetail = res.data.data.article;
            this.$message.success("Success: get article detail");
            if (this.selectedArticleDetail.video !== undefined && this.selectedArticleDetail.video !== '') {
              setTimeout(() => {
                this.createVideo();
              }, 1000);
            }
          } else {
            console.log("Error: get article detail", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get article detail", error);
          this.$message.error("Error: get article detail", error);
        });
    },
    getArticleStatus(index, row) {
      this.selectedArticle = this.tableData[index];
      this.dialogStatus = true;
      let data = {
        aid: this.selectedArticle.aid
      };
      this.$axios
        .get("/api/article/status?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get article status", res);
            this.selectedArticleStatus = [
              {
                type: "Agree",
                num: res.data.data.article_status[0].agreeNum
              },
              {
                type: "Comment",
                num: res.data.data.article_status[0].commentNum
              },
              {
                type: "Read",
                num: res.data.data.article_status[0].readNum
              },
              {
                type: "Share",
                num: res.data.data.article_status[0].shareNum
              }
            ];
            res.data.data.article_status[0];
            this.$message.success("Success: get article status");
          } else {
            console.log("Error: get article status", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get article status", error);
          this.$message.error("Error: get article status", error);
        });
    }
  }
};
</script>

<style>
</style>
