FROM ghcr.io/windmill-labs/windmill:1.392.0

# 安裝 gosu + 建立 windmill 用戶 (uid=1000, gid=1000)
RUN apt-get update && apt-get install -y gosu \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 -s /bin/bash windmill

# 切換到 windmill 執行（但保留 root 入口）
USER root
