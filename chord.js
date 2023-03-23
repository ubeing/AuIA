// 基于UDP协议实现p2p的chord算法
// 作者：李春阳
// 日期：2017-12-20

// 依赖
var dgram = require('dgram');
var crypto = require('crypto');
var fs = require('fs');
var readline = require('readline');

// 读取配置文件
var config = JSON.parse(fs.readFileSync('config.json', 'utf8'));

// 读取命令行参数
var args = process.argv.splice(2);
var port = args[0];
var id = args[1];

// 创建socket
var socket = dgram.createSocket('udp4');

// 保存节点信息
var node = {
    id: id,
    port: port,
    finger: [],
    successor: null,
    predecessor: null
};

// 保存节点信息
var nodes = [];

// 保存文件信息
var files = [];

// 生成随机ID
function randomId() {
    return crypto.randomBytes(20).toString('hex');
}

// 生成随机端口
function randomPort() {
    return Math.floor(Math.random() * 10000 + 10000);
}

// 生成随机节点
function randomNode() {
    return {
        id: randomId(),
        port: randomPort()
    };
}

// 生成随机文件
function randomFile() {
    return {
        id: randomId(),
        name: randomId() + '.txt',
        content: randomId()
    };
}

// 初始化节点
function initNode() {
    // 生成随机ID
    if (!node.id) {
        node.id = randomId();
    }

    // 生成随机端口
    if (!node.port) {
        node.port = randomPort();
    }

    // 初始化finger表
    for (var i = 0; i < 160; i++) {
        node.finger[i] = node;
    }

    // 初始化successor和predecessor
    node.successor = node;
    node.predecessor = node;
}

// 初始化文件
function initFile() {
    // 生成随机文件
    for (var i = 0; i < 10; i++) {
        files.push(randomFile());
    }
}

