FROM apache/airflow:2.10.0-python3.11

USER root

# Install OpenJDK-17
RUN find /etc/apt -name '*.sources' -o -name 'sources.list' | xargs -r sed -i 's|http://deb.debian.org|https://deb.debian.org|g' && \
    apt-get update && \
    apt-get install -y openjdk-17-jdk procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sfn "$(dirname "$(dirname "$(readlink -f "$(which javac)")")")" /usr/lib/jvm/default-java

# Set JAVA_HOME (resolved above so it works on both amd64 and arm64 hosts)
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

USER airflow

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt