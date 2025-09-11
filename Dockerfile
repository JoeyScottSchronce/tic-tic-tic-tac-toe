# syntax=docker/dockerfile:1

# Stage 1: Dependency setup (system packages, Python, python-for-android)
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y --no-install-recommends \
    python3.11 python3.11-venv python3.11-dev \
    python3-pip build-essential libffi-dev libssl-dev \
    openjdk-17-jdk unzip zip git wget \
    libncurses5 libncurses5-dev zlib1g-dev \
    libsqlite3-dev libgdbm-dev libbz2-dev \
    libreadline-dev liblzma-dev libgmp-dev \
    autoconf automake libtool \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install python-for-android
RUN git clone --branch develop https://github.com/kivy/python-for-android.git /p4a
WORKDIR /p4a
RUN pip3 install --upgrade pip
RUN pip3 install .

# Stage 2: SDK/NDK setup
FROM builder AS sdk

ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_NDK_HOME=/opt/android-sdk/ndk/25.2.9519653
ENV PATH="$ANDROID_SDK_ROOT/platform-tools:$PATH"
ENV PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH"
ENV PATH="$ANDROID_SDK_ROOT/build-tools/33.0.0:$PATH"
ENV PATH="$ANDROID_NDK_HOME:$PATH"

RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools \
    && cd $ANDROID_SDK_ROOT/cmdline-tools \
    && wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip \
    && unzip tools.zip \
    && rm tools.zip \
    && mv cmdline-tools latest

RUN yes | $ANDROID_SDK_ROOT/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_SDK_ROOT \
    "platform-tools" \
    "platforms;android-33" \
    "build-tools;33.0.0" \
    "ndk;25.2.9519653"

# Stage 3: App build
FROM sdk

WORKDIR /app
COPY . /app
COPY icon.png /app/icon.png
RUN chmod -R 755 /app

# Build APK on container start
# This command can be modified as needed for other build options
CMD ["p4a","apk", "--private", "/app", "--package", \
    "org.james.ticticboom", "--name", "TicTicBoom", \
    "--version", "1.0", "--bootstrap", "sdl2", \
    "--requirements", "python3,kivy,requests,filetype,certifi,idna,urllib3", \
    "--arch", "armeabi-v7a", "--ndk-api", "21", "--android-api", \
    "33", "--sdk-dir", "/opt/android-sdk", "--ndk-dir", \
    "/opt/android-sdk/ndk/25.2.9519653", "--icon", "/app/icon.png"]
