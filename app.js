'use strict';

const RAW_BASE = 'https://raw.githubusercontent.com/MaddestAlistar/LiangyouChannels/main/';
const PLATFORMS = [
  {id: 'douyin', label: '抖音'}, {id: 'douyu', label: '斗鱼'},
  {id: 'huya', label: '虎牙'}, {id: 'bilibili', label: 'B站'}, {id: 'yy', label: 'YY'}
];
const container = document.getElementById('channels');
const toast = document.getElementById('toast');
let toastTimer;

function notify(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.add('visible');
  toastTimer = setTimeout(() => toast.classList.remove('visible'), 2700);
}

function legacyCopy(value) {
  const previous = document.activeElement;
  const selection = window.getSelection();
  const ranges = [];
  if (selection) for (let i = 0; i < selection.rangeCount; i++) ranges.push(selection.getRangeAt(i).cloneRange());
  const input = document.createElement('textarea');
  input.value = value;
  input.readOnly = true;
  input.style.cssText = 'position:fixed;top:0;left:0;opacity:0;font-size:16px';
  document.body.append(input);
  input.focus({preventScroll: true});
  input.select();
  input.setSelectionRange(0, value.length);
  let copied = false;
  try { copied = document.execCommand('copy'); } catch (_) { /* Use the manual dialog. */ }
  input.remove();
  if (previous instanceof HTMLElement) previous.focus({preventScroll: true});
  if (selection) { selection.removeAllRanges(); ranges.forEach(range => selection.addRange(range)); }
  return copied;
}

async function copyChannel(channel, card) {
  // Every identifier is an opaque string. Do not trim punctuation, lowercase it, or parse it as a number.
  const value = channel.copyValue;
  let copied = false;
  if (navigator.clipboard && window.isSecureContext) {
    try { await navigator.clipboard.writeText(value); copied = true; } catch (_) { /* Older Safari and embedded browsers. */ }
  }
  if (!copied) copied = legacyCopy(value);
  if (!copied) {
    document.getElementById('manual-copy-title').textContent = channel.name + ' · ' + channel.platformLabel;
    const input = document.getElementById('manual-copy-value');
    input.value = value;
    document.getElementById('manual-copy').showModal();
    input.focus();
    input.select();
    input.setSelectionRange(0, value.length);
    return;
  }
  card.classList.add('copied');
  setTimeout(() => card.classList.remove('copied'), 2200);
  notify('已复制 ' + channel.name + ' · ' + value);
}

function copyGlyph() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', 'M9 7V4h11v13h-3M4 8h12v13H4z');
  svg.append(path);
  return svg;
}

function render(channels) {
  const fragment = document.createDocumentFragment();
  for (const platform of PLATFORMS) {
    const entries = channels.filter(channel => channel.platform === platform.id);
    if (!entries.length) continue;
    const section = document.createElement('section');
    section.className = 'channel-section ' + platform.id;
    section.id = platform.id;
    section.setAttribute('aria-labelledby', platform.id + '-heading');
    const header = document.createElement('div');
    header.className = 'section-heading';
    const heading = document.createElement('h2');
    heading.id = platform.id + '-heading';
    const dot = document.createElement('span');
    dot.className = 'platform-dot';
    dot.setAttribute('aria-hidden', 'true');
    heading.append(dot, document.createTextNode(platform.label));
    const count = document.createElement('span');
    count.textContent = entries.length + ' 个频道';
    header.append(heading, count);
    const grid = document.createElement('div');
    grid.className = 'channel-grid';
    for (const channel of entries) {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'channel-card';
      card.dataset.channelId = channel.id;
      card.setAttribute('aria-label', '复制' + channel.name + '的' + platform.label + '房间号：' + channel.copyValue);
      card.title = '点击复制：' + channel.copyValue;
      const wrap = document.createElement('span');
      wrap.className = 'image-wrap';
      const image = document.createElement('img');
      image.src = './' + channel.icon;
      image.alt = channel.name + ' · ' + platform.label;
      image.width = 256;
      image.height = 256;
      image.loading = platform.id === 'douyin' ? 'eager' : 'lazy';
      image.decoding = 'async';
      image.addEventListener('error', () => {
        if (image.dataset.retried) return;
        image.dataset.retried = 'true';
        image.src = channel.avatar;
      });
      wrap.append(image);
      const name = document.createElement('span');
      name.className = 'channel-name';
      name.textContent = channel.name;
      const room = document.createElement('span');
      room.className = 'channel-room';
      const value = document.createElement('code');
      value.textContent = channel.copyValue;
      room.append(value, copyGlyph());
      card.append(wrap, name, room);
      card.addEventListener('click', () => copyChannel(channel, card));
      grid.append(card);
    }
    section.append(header, grid);
    fragment.append(section);
    const chipCount = document.querySelector('[data-count="' + platform.id + '"]');
    if (chipCount) chipCount.textContent = String(entries.length);
  }
  container.replaceChildren(fragment);
  container.setAttribute('aria-busy', 'false');
  document.getElementById('total-count').textContent = String(channels.length);
}

async function loadChannels() {
  container.setAttribute('aria-busy', 'true');
  try {
    let response = await fetch('./channel-data.json', {cache: 'no-cache'});
    if (!response.ok) response = await fetch(RAW_BASE + 'channel-data.json', {cache: 'no-cache'});
    if (!response.ok) throw new Error('Could not read channels');
    const data = await response.json();
    const channels = Array.isArray(data) ? data : data.channels;
    if (!Array.isArray(channels) || !channels.length || channels.some(channel =>
      typeof channel.copyValue !== 'string' || typeof channel.roomId !== 'string' ||
      channel.copyValue !== channel.roomId || !PLATFORMS.some(platform => platform.id === channel.platform) ||
      typeof channel.icon !== 'string' || !/^icons\/[a-z]+\/[\w-]+\.png$/.test(channel.icon))) {
      throw new Error('Invalid channel data');
    }
    if (typeof data.description === 'string') {
      document.getElementById('collection-description').textContent = data.description;
    }
    render(channels);
  } catch (_) {
    const error = document.createElement('p');
    error.className = 'error-message';
    error.textContent = '频道暂时读取失败。';
    const retry = document.createElement('button');
    retry.type = 'button';
    retry.textContent = '重新读取';
    retry.addEventListener('click', loadChannels);
    error.append(retry);
    container.replaceChildren(error);
    container.setAttribute('aria-busy', 'false');
  }
}

loadChannels();
