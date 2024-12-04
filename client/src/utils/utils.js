// utils.js

/**
 * 检查是否为移动设备
 * @returns {boolean} 是否为移动设备
 */
export const checkIsMobile = () => {
    return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
};

/**
 * 随机生成颜色
 * @returns {string} 随机生成的颜色值
 */
export const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

import { ElNotification, ElMessage } from 'element-plus';

/**
 * 显示通知消息
 * @param {string} message - 消息内容
 * @param {boolean} isMobile - 是否为移动设备
 */
export const showNotification = (message, isMobile, customClass = '') => {
    if (!isMobile) {
        ElNotification({
            title: "Success",
            message: message,
            type: "success",
            showClose: false,
            position: "top-left",
        });
    } else {
        ElMessage({
            message: message,
            type: "success",
            plain: true,
            customClass: customClass,

        });
    }
};
