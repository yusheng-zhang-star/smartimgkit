/**
 * 批量任务内存安全工具 - 修复批量处理图片时内存泄漏问题
 * 自动回收ObjectURL，限制并发，防止低配浏览器崩溃
 */
export class SafeObjectUrl {
  #url = null;
  #blob = null;

  constructor(blob) {
    this.#blob = blob;
    this.#url = URL.createObjectURL(blob);
  }

  get url() {
    return this.#url;
  }

  release() {
    if (this.#url) {
      URL.revokeObjectURL(this.#url);
      this.#url = null;
    }
    this.#blob = null;
  }
}

export class BatchTaskQueue {
  constructor(maxConcurrent = 4) {
    this.maxConcurrent = maxConcurrent;
    this.runningCount = 0;
    this.taskQueue = [];
    this.cancelFlag = false;
  }

  add(taskPromiseFn) {
    return new Promise((resolve, reject) => {
      if (this.cancelFlag) return reject(new Error("Batch task canceled"));
      this.taskQueue.push({ taskPromiseFn, resolve, reject });
      this._next();
    });
  }

  _next() {
    if (this.cancelFlag) return;
    if (this.runningCount >= this.maxConcurrent || this.taskQueue.length === 0) return;
    this.runningCount += 1;
    const item = this.taskQueue.shift();
    item.taskPromiseFn()
      .then(res => item.resolve(res))
      .catch(err => item.reject(err))
      .finally(() => {
        this.runningCount -= 1;
        this._next();
      });
  }

  cancelAll() {
    this.cancelFlag = true;
    this.taskQueue.forEach(t => t.reject(new Error("Batch task canceled")));
    this.taskQueue = [];
  }
}
