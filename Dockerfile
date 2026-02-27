FROM grandnode/grandnode2:latest

# Install Chinese locale support
USER root
RUN apt-get update && apt-get install -y --no-install-recommends locales && \
    sed -i '/zh_CN.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen zh_CN.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

# Copy Chinese locale files
COPY locales/ /app/App_Data/Localization/

# Copy plugin configs
COPY plugins/ /app/Plugins/

EXPOSE 5000

ENTRYPOINT ["dotnet", "GrandNode.Web.dll"]
