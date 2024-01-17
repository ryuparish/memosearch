<h1 align="center">Welcome to Memosearch 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="something" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="#" target="_blank">
    <img alt="License: BSD--2" src="https://img.shields.io/badge/License-BSD--2-yellow.svg" />
  </a>
</p>

![alt text](https://github.com/ryuparish/memosearch/blob/main/Memosearch%20Image.png?raw=true)

> A search engine and note taking tool for screenshots, links, and text notes.

### 🏠 [Homepage](https://github.com/ryuparish/memosearch)

### ✨ [Demo](something)

## Install
### Backend
```sh
cd memosearch/src/backend/src
pip install -e .
flask --app memosearch run (ensure server can start)
```
### Frontend
```sh
cd memosearch/src/frontend
npm install src
npm start (ensure server can start)
```
### Finally
```sh
cd memosearch/src
./MemoSearch.command (run servers together)
```
## Usage
I like to set the MemoSearch.command script as an alias like this:
(in my .zshrc)
```sh
alias ms="bash [path/to/Memosearch.command]"
```
then in my terminal I run:
```sh
ms
```

## Run tests

```sh
cd memosearch/src/backend/src
pytest
coverage -m pytest
coverage report (view code coverage)j
```

## Author

👤 **Ryu Parish**

* Website: https://ryuparish.github.io/ryus_website/
* Github: [@ryuparish](https://github.com/ryuparish)
* LinkedIn: [@https:\/\/www.linkedin.com\/in\/ryu-parish-b8894b15b\/](https://linkedin.com/in/https:\/\/www.linkedin.com\/in\/ryu-parish-b8894b15b\/)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/ryuparish/memosearch/issues). 

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
