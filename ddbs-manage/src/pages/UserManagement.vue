<template>
  <div class="main-container">
    <div class="page-header">User Management</div>
    <div class="page-content">
      <div style="display: flex; margin-bottom: 30px;">
        <el-button @click="addUser"><i class="el-icon-plus"></i> New</el-button>
        <el-input style="width: 200px; margin-left: 20px;" v-model="uid" placeholder="uid"></el-input>
        <el-button style="width: 100px; margin-left: 70px;" type="primary" @click="getUser">Go</el-button>
      </div>

      <el-table
        :data="tableData"
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
        <el-table-column label="Depart.">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.dept }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Grade">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.grade }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Lang." width="60">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.language }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Role">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.role }}</span>
          </template>
        </el-table-column>
        <el-table-column label="PreferTag">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.preferTags }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Credits" width="70">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.obtainedCredits }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Operations" width="180">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="editUser(scope.$index, scope.row)">
              Edit
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deleteUser(scope.$index, scope.row)">
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <el-dialog
      :title="ifCreate ? 'Add New User' : selectedUser.name"
      :visible.sync="inputDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="37%">
      <div>
        <el-form label-position="top" label-width="80px" :model="selectedUserEdit">
          <el-form-item label="UID">
            <el-input v-model="selectedUserEdit.uid"></el-input>
          </el-form-item>
          <el-form-item label="Name">
            <el-input v-model="selectedUserEdit.name"></el-input>
          </el-form-item>
          <el-form-item label="Region">
            <el-input v-model="selectedUserEdit.region"></el-input>
          </el-form-item>
          <el-form-item label="Gender">
            <el-input v-model="selectedUserEdit.gender"></el-input>
          </el-form-item>
          <el-form-item label="Email">
            <el-input v-model="selectedUserEdit.email"></el-input>
          </el-form-item>
          <el-form-item label="Phone">
            <el-input v-model="selectedUserEdit.phone"></el-input>
          </el-form-item>
          <el-form-item label="Department">
            <el-input v-model="selectedUserEdit.dept"></el-input>
          </el-form-item>
          <el-form-item label="Grade">
            <el-input v-model="selectedUserEdit.grade"></el-input>
          </el-form-item>
          <el-form-item label="Language">
            <el-input v-model="selectedUserEdit.language"></el-input>
          </el-form-item>
          <el-form-item label="Role">
            <el-input v-model="selectedUserEdit.role"></el-input>
          </el-form-item>
          <el-form-item label="Prefer Tags">
            <el-input v-model="selectedUserEdit.preferTags"></el-input>
          </el-form-item>
          <el-form-item label="Obtained Credits">
            <el-input v-model="selectedUserEdit.obtainedCredits"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="inputDialog = false">Cancel</el-button>
        <el-button type="primary" @click="postUser">OK</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
import qs from "qs";

export default {
  name: 'UserManagement',
  data () {
    return {
      ifCreate: false,
      inputDialog: false,
      tableData: [],
      selectedUser: {},
      selectedUserEdit: {},
      uid: '1',
    }
  },
  created () {
    this.getUser()
  },
  methods: {
    getUser() {
      let data = {
        uid: this.uid
      };
      this.$axios
        .get("/api/user?" + qs.stringify(data))
        .then(res => {
          if (res.data.status === "success") {
            console.log("Success: get user(s)", res);
            this.tableData = res.data.data.user;
            this.$message.success("Success: get user(s)");
          } else {
            console.log("Error: get user(s)", res);
            this.$message.error(res.data.msg);
          }
        })
        .catch(error => {
          console.log("Error: get user(s)", error);
          this.$message.error("Error: get user(s)", error);
        });
    },
    addUser() {
      this.ifCreate = true;
      this.selectedUserEdit = {
        uid: '',
        name: '',
        region: '',
        gender: '',
        email: '',
        phone: '',
        dept: '',
        grade: '',
        language: '',
        role: '',
        preferTags: '',
        obtainedCredits: ''
      }
      this.inputDialog = true;
    },
    editUser(index, row) {
      this.ifCreate = false;
      this.selectedUser = row;
      this.selectedUserEdit = Object.assign({}, row);
      this.inputDialog = true;
    },
    postUser() {
      let user = this.selectedUserEdit
      let formData = new FormData()
      formData.append('action', this.ifCreate ? 'add' : 'edit')
      formData.append('uid', user.uid)
      formData.append('name', user.name)
      formData.append('region', user.region)
      formData.append('gender', user.gender)
      formData.append('email', user.email)
      formData.append('phone', user.phone)
      formData.append('dept', user.dept)
      formData.append('grade', user.grade)
      formData.append('language', user.language)
      formData.append('role', user.role)
      formData.append('preferTags', user.preferTags)
      formData.append('obtainedCredits', user.obtainedCredits)

      this.$axios.post('/api/user', formData).then(res => {
        if (res.data.status === 'success') {
          console.log('Success: add user', res)
          this.getUser()
          this.$message.success('Success: add user')
          this.inputDialog = false
        } else {
          console.log('Error: add user', res)
          this.$message.error('Error: add user')
        }
      }).catch(error => {
          console.log('Error: add user', error)
          this.$message.error('Error: add user')
      })
    },
    deleteUser(index, row)  {
      let formData = new FormData()
      formData.append('uid', row.uid);

      this.$axios.delete('/api/user', {data: {uid: row.uid}}).then(res => {
        if (res.data.status === 'success') {
          console.log('Success: delete user', res)
          this.getUser()
          this.$message.success('Success: delete user')
        } else {
          console.log('Error: add user', res)
          this.$message.error('Error: delete user')
        }
      }).catch(error => {
          console.log('Error: add user', error)
          this.$message.error('Error: delete user')
      })
    }
  }
}
</script>

<style scoped>

</style>