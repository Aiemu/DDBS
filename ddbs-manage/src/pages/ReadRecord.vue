<template>
  <div class="main-container">
    <div class="page-header">Read Record</div>
    <div class="page-content">
      <div style="display: flex; margin-bottom: 30px;">
        <el-select @change="recordOptionChange" style="width: 100px;" v-model="selectedRecord" placeholder="请选择">
          <el-option
            v-for="item in recordOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <el-input style="width: 150px; margin-left: 20px;" v-model="id" :placeholder="selectedRecord"></el-input>
        <el-button style="width: 70px; margin-left: 70px;" type="primary" @click="handleGo">Go</el-button>
      </div>
      <div v-if="selectedRecord === 'uid'" style="margin-bottom: 15px;">
       <span class="label-yellow" style="font-weight: bold;">{{ 'user' + tmpId }}</span> has read the following articles (<span class="label-yellow" style="font-weight: bold;">{{ tableData.length }}</span> in total):
      </div>
      <div v-if="selectedRecord === 'aid'" style="margin-bottom: 15px;">
        <span class="label-yellow" style="font-weight: bold;">{{ 'article' + tmpId }}</span> has been read by the following users (<span class="label-yellow" style="font-weight: bold;">{{ tableDataUser.length }}</span> in total):
      </div>
      <el-table
        v-if="selectedRecord === 'uid'"
        :data="tableData"
        style="width: 95%"
        height="460"
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
        <el-table-column label="Operations" width="90">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="getArticleDetail(scope.$index, scope.row)"
            >
              Details
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

      <el-table
        v-if="selectedRecord === 'aid'"
        :data="tableDataUser"
        style="width: 95%"
        height="460"
        :border="true"
      >
        <el-table-column label="UID" width="70">
          <template slot-scope="scope">
            <span>{{ scope.row.uid }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Name">
          <template slot-scope="scope">
            <el-tooltip
              class="item"
              effect="dark"
              :content="'email: ' + scope.row.email + ', \nphone: ' + scope.row.phone"
              placement="top-start"
            >
              <span style="font-weight: bold; font-style: italic;">{{
                scope.row.name
              }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="Gender">
          <template slot-scope="scope">
            <span>{{ scope.row.gender }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Region">
          <template slot-scope="scope">
            <span
              v-if="scope.row.region === 'Beijing'"
              class="label-green">
              {{ scope.row.region }}
            </span>
            <span
              v-else-if="scope.row.region === 'Hong Kong'"
              class="label-blue">
              {{ scope.row.region }}
            </span>
            <span
              v-else class="label-yellow">
              {{ scope.row.region }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="Department">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.dept }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Grade">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.grade }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Language">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.language }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Role">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.role }}</span>
          </template>
        </el-table-column>
        <el-table-column label="PreferTags">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.preferTags }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Credits">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.obtainedCredits }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="90">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="getArticleDetail(scope.$index, scope.row)"
            >
              Details
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
  </div>
</template>

<script>
import qs from "qs";
import flvjs from "flv.js";

export default {
  name: "ReadRecord",
  data() {
    return {
      dialogDetail: false,
      selectedArticle: {},
      selectedArticleDetail: {},
      id: '1',
      tmpId: '1',
      recordOptions: [
        {
          value: 'uid',
          label: 'User'
        },
        {
          value: 'aid',
          label: 'Article'
        }
      ],
      selectedRecord: 'uid',
      tableData: [],
      tableDataUser: []
    };
  },
  created() {
    this.getUserRead();
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
    recordOptionChange(option) {
      if (option.value === 'uid') {
        this.getUserRead();
      } else {
        this.getArticleRead();
      }
    },
    handleGo() {
      if (this.selectedRecord === 'uid') {
        this.getUserRead();
      } else {
        this.getArticleRead();
      }
    },
    getUserRead() {
      let data = {
        uid: this.id
      };
      this.$axios
        .get("/api/record/user?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get article(s) read by the user", res);
            this.tableData = res.data.data.article;
            this.tmpId = this.id;
            this.$message.success("Success: get article(s) read by the user");
          } else {
            console.log("Error: get article(s) read by the user", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get article(s) read by the user", error);
          this.$message.error("Error: get article(s) read by the user", error);
        });
    },
    getArticleRead() {
      let data = {
        aid: this.id
      };
      this.$axios
        .get("/api/record/article?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get user(s) who read the book", res);
            this.tableDataUser = res.data.data.user;
            this.tmpId = this.id;
            this.$message.success("Success: get user(s) who read the book");
          } else {
            console.log("Error: get user(s) who read the book", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get user(s) who read the book", error);
          this.$message.error("Error: get user(s) who read the book", error);
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
    }
  }
};
</script>

<style>
</style>
