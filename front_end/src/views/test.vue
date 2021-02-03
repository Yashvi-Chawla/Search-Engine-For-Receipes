<template>
  <div id="app">
    <div class="home col">
      <section class="first col">
        <el-autocomplete
          class="search"
          v-model="inputValue"
          :fetch-suggestions="querySearch"
          placeholder="请输入内容"
          @select="handleSelect"
        >
          <!--这里是搜索框的内容-->
          <!--select这里会显示所选的内容-->
          <el-button slot="append" icon="el-icon-search" @click="handleSearchClick"></el-button>
        </el-autocomplete>
        <!-- 下拉折叠区域 -->
        <section class="collapse-area">
          <div class="triangle">
            <div class="triangle-item" @click="foldAll" :class="{'rotate':isRotate}"></div>
          </div>
          <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item :name="index" v-for="(item,index) in checkData" :key="index">
              <p style="margin-left:15px;" slot="title">
                <el-icon
                  class="el-icon-arrow-right"
                  :class="{'rotate':activeNames.includes(index)}"
                ></el-icon>
                {{item.title}}
              </p>
              <el-row>
                <el-col :span="8" v-for="(sub,key) in item.check" :key="key">
                  <el-checkbox :label="sub" @change="handleAddCheck(sub)"></el-checkbox>
                </el-col>
              </el-row>
            </el-collapse-item>
          </el-collapse>
        </section>
      </section>
      <!-- 图片展示区域 -->
      <section class="second col">
        <transition name="el-fade-in-linear">
          <div class="img-contaienr row" v-show="imgs.length">
            <div
              class="img-item"
              v-for="item in imgs"
              :key="item.id"
              @mouseover="() => handleImageHover(item)"
              @mouseout="() => handleImageOut(item)"
            >
              <el-image :src="item.src">
                <div slot="placeholder" class="image-slot">
                  <!-- loading<span class="dot">...</span> -->
                </div>
              </el-image>
              <div class="img-hover-info" v-show="item.isHover">{{ item.desc }}</div>
            </div>
          </div>
        </transition>
        <el-button class="footer-btn" icon="el-icon-refresh-right" circle @click="refreshClick"></el-button>
      </section>
    </div>
  </div>
</template>

<script>
import DataList from "../assets/dataList.js";
const testData1 = [
  {
    id: 1,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 2,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 3,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 4,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 5,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 6,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 7,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 8,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  },
  {
    id: 9,
    src:
      "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
    desc: "图片描述"
  }
];
const testData2 = [
  {
    id: 1,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 2,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 3,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 4,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 5,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 6,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 7,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 8,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  },
  {
    id: 9,
    src:
      "https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg",
    desc: "图片描述2"
  }
];
const tempFlag = {
  search: true,
  refresh: true
};
// @ is an alias to /src
import axios from "axios";
export default {
  name: "home",
  components: {},
  data() {
    return {
      imgs: [],
      inputValue: "",
      activeNames: [],
      selectCheck: [],
      checkData: DataList.checkBox,
      checkList: ["chicken"]
    };
  },
  computed: {
    isRotate() {
      // var index = this.activeNames.indexOf("0");
      if (this.activeNames.length > 0) {
        return true;
      } else {
        return false;
      }
    }
  },
  mounted() {
    this.getData();
    this.imgs = testData1;
  },
  methods: {
    //监听页面下滚150px
    handleScroll(e) {
      const scrollTop =
        document.documentElement.scrollTop || document.body.Scroller;
      this.isScroll = scrollTop > 200;
    },
    handleAddCheck(value) {
      var index = this.selectCheck.indexOf(value);
      if (index >= 0) {
        this.selectCheck.splice(index, 1);
      } else {
        this.selectCheck.push(value);
      }
    },
    getData() {
      axios
        .get("http://wthrcdn.etouch.cn/weather_mini", {
          // 传递参数
          params: {
            queryBox: "spicy" /*这里传递进去的querybox和checkbox*/,
            checkBox: "chicken"
          }
        })
        .then(response => {
          // 请求成功
          let res = response.data;
          console.log(res);
          //这个res就是请求回来的数据，可以在控制台看到，下面是修改了一条图片描述
          this.imgs[0].desc = res.data.ganmao;
          this.imgs[0].src = res.data.ganmao;
        });
    },
    handleSearchClick() {
      tempFlag.refresh = !tempFlag.refresh;
      this.imgs = tempFlag.refresh ? testData1 : testData2;
    },
    refreshClick() {
      tempFlag.search = !tempFlag.search;
      const arr = this.imgs.concat(tempFlag.search ? testData1 : testData2);
      this.imgs = arr;
    },
    handleImageHover(item) {
      this.$set(item, "isHover", true);
    },
    handleImageOut(item) {
      this.$set(item, "isHover", false);
    },
    querySearch(queryString, cb) {
      var checkList = this.checkList.map(item => ({ value: item }));
      var results = queryString
        ? checkList.filter(this.createFilter(queryString))
        : checkList;
      cb(results);
    },
    createFilter(queryString) {
      return checkList => {
        return (
          checkList.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        );
      };
    },
    handleSelect(item) {
      console.log(item);
    },
    handleChange() {},
    foldAll() {
      this.activeNames = [0];
    }
  }
};
</script>

<style lang="less" scoped>
html {
  padding: 0px;
  margin: 0px;
} /*这是把白边去掉的方法*/

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.isScroll {
  background: linear-gradient(
    to right,
    rgba(30, 87, 153, 0.8) 0%,
    rgba(30, 87, 153, 0.8) 44%,
    rgba(41, 137, 216, 0.8) 94%
  ) !important; /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc1e5799', endColorstr='#cc2989d8',GradientType=1 );
}
.col{
display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.row{
   display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-items: center; 
}
.home {
  //背景
  .first {
    height: 100vh;
    padding: 250px 350px  250px 350px;
    width: 100%;
    background: url("https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg");
    background-repeat: round;
    background-attachment: fixed;
    .search {
      width: 500px;
      margin-top: 30px;
    }
    .collapse-area {
      margin-top: 70px;
      width:1250px;
      opacity: 0.5;
    }
  }

  .second {
      height:100vh;
      width: 100vw;
      
      background: linear-gradient(
    to right,
    rgba(30, 87, 153, 0.8) 0%,
    rgba(30, 87, 153, 0.8) 44%,
    rgba(41, 137, 216, 0.8) 94%
  ) !important; /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc1e5799', endColorstr='#cc2989d8',GradientType=1 );
    min-height: 700px;
    .img-contaienr {
    width: 1250px;
      flex-wrap: wrap;
      margin-top: 80px;
      .img-item {
        width: 380px;
        margin: 0px 2px;
        position: relative;
        .img-hover-info {
          width: 380px;
          height: 253px;
          position: absolute;
          top: 0px;
          left: 0px;
          background: rgba(255, 165, 79, 0.5);
          text-align: center;
          line-height: 253px;
          color: #fff;
        }
      }
    }
  }
  .footer-btn {
    margin-top: 30px;
  }
}
.triangle {
  width: 100%;
  height: 30px;
  line-height: 30px;
  font-size: 30px;
  text-align: left;
  .triangle-item {
    width: 0;
    height: 0;
    overflow: hidden;
    border-left: 10px solid #000;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    transition: transform 0.2s ease-in;
  }
}
/deep/.el-collapse-item__arrow {
  display: none !important;
}
.rotate {
  transform: rotate(90deg);
  transition: transform 0.2s ease-in;
}
</style>
