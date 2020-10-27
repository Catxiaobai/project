<template>
  <div id="common-aside">
    <div id="aside-content">
      <el-menu id="menu" router :default-active="$route.path">
        <el-submenu id="hasChildren" :index="item.path" v-for="item in hasChildren" :key="item.path" @click="clickMenu(item)">
          <template slot="title" id="title">
            <i :class="'el-icon-' + item.icon"></i>
            <span class="name">{{ item.label }}</span>
          </template>
          <el-menu-item-group id="child">
            <el-menu-item :index="subItem.path" v-for="subItem in item.children" :key="subItem.path" @click="clickMenu(subItem)">
              <template slot="title">
                <i :class="'el-icon-caret-right'"></i>
                <span class="name">{{ subItem.label }}</span>
              </template>
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-menu-item id="noChildren" :index="item.path" v-for="item in noChildren" :key="item.path" @click="clickMenu(item)">
          <i :class="'el-icon-' + item.icon"></i>
          <span class="name" slot="title">{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div id="aside-right"></div>
  </div>
</template>

<script>
export default {
  name: 'CommonAside.vue',
  data() {
    return {
      asideMenu: [
        {
          path: '/infoManage/system',
          name: 'system',
          label: '系统管理',
          icon: 's-claim',
          children: [
            {
              path: '/personnel',
              name: 'personnel',
              label: '人员管理'
            },
            {
              path: '/authority',
              name: 'authority',
              label: '权限管理'
            },
            {
              path: '/tools',
              name: 'tools',
              label: '工具说明'
            }
          ]
        },
        {
          path: '/item',
          name: 'item',
          label: '项目管理',
          icon: 's-claim'
        }
      ]
    }
  },
  mounted() {
    this.getMenu()
  },
  methods: {
    clickMenu(item) {
      if (this.$route.name !== item.name) {
        this.$router.push({ name: item.name })
      }
      // this.$store.commit('selectMenu', item)
    },
    getMenu() {
      this.bus.$on('transferMenuData', msg => {
        this.asideMenu = msg
      })
    }
  },
  computed: {
    noChildren() {
      return this.asideMenu.filter(item => !item.children)
    },
    hasChildren() {
      // console.log(
      //   'hasChildren',
      //   this.asideMenu.filter(item => item.children)
      // )
      return this.asideMenu.filter(item => item.children)
    },
    noGrandchildren() {
      console.log(
        'noGrandchildren',
        this.asideMenu.filter(item => item.children).filter(item => item.children.children)
      )
      return this.asideMenu.filter(item => item.children).filter(item => !item.children.children)
    },
    hasGrandchildren() {
      return this.asideMenu.filter(item => item.children.children)
    }
  }
}
</script>

<style scoped lang="scss">
#common-aside {
  background: lightyellow;
  width: 100%;
  height: 634px;
  font-weight: bold;
  display: flex;
  #aside-content {
    width: 100%;
    height: 100%;
    #menu {
      height: 100%;
      //background: skyblue;
      #noChildren {
        //background: yellow;
        font-size: 18px;
      }
      #hasChildren {
        //background: moccasin;
        #child {
          background: whitesmoke;
        }
      }
      .name {
        font-size: 14px;
      }
    }
  }
  #aside-right {
    background: skyblue;
    width: 5px;
    height: 100%;
  }
}
</style>
