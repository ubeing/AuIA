// Waiting the Github passing ...
// 需要写一个冒泡算法的代码段
// 1. 从第一个元素开始，比较相邻的两个元素，如果第一个比第二个大，就交换他们两个。
// 2. 对每一对相邻元素做同样的工作，从开始第一对到结尾的最后一对。这步做完后，最后的元素会是最大的数。
// 3. 针对所有的元素重复以上的步骤，除了最后一个。
// 4. 重复步骤1~3，直到排序完成。  
// 5. 代码实现
function bubbleSort(arr) {
    var i = arr.length, j;
    var tempExchangVal;
    while (i > 0) {
        for (j = 0; j < i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                tempExchangVal = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tempExchangVal;
            }
        }
        i--;
    }
    return arr;
}

const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

console.log(bubbleSort(arr));

