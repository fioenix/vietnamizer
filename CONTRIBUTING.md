# Đóng góp cho vietnamizer

Người dùng có thể gửi ca sửa sai hoặc đề xuất sửa bằng issue và pull request. Một ca hữu ích gồm
thể loại, người đọc, đoạn gốc, kết quả của skill, bản đối chiếu và lý do khác biệt. Chỉ gửi văn bản
mày có quyền công bố; thay dữ kiện riêng bằng ví dụ giả lập trước khi gửi.

[GitHub Issues](https://github.com/fioenix/vietnamizer/issues) dùng mẫu báo lỗi trong
`.github/ISSUE_TEMPLATE/bug_report.yml`. Ghi phiên bản và nguồn cài, client/provider, các bước tái
hiện, kết quả mong đợi/thực tế và ví dụ tối thiểu đã ẩn dữ liệu. Nếu không biết phiên bản hoặc
model thì ghi rõ; lỗi cài đặt không bắt buộc có văn bản đầu vào.

Không đăng API key, token, dữ liệu cá nhân, tài liệu nội bộ hoặc nội dung nhạy cảm. Không cần
gửi toàn bộ prompt, log hay tài liệu. Lỗi bảo mật dùng [kênh riêng trong SECURITY.md](SECURITY.md),
không dùng Issues hoặc pull request công khai.

`SKILL.md` sở hữu điều phối/chốt; bốn catalog V/T trong `references/` sở hữu nội dung quy tắc chung; `profiles/` sở hữu quy tắc theo thể loại. Xem [AGENTS.md](AGENTS.md)
trước khi sửa rule. Sở thích văn phong cá nhân không được đưa vào calibration dùng chung.

## Chạy kiểm tra offline

Skill Markdown dùng trực tiếp, không cần build. Test đóng gói dùng Python 3.12 và standard library;
không cần SDK, `uv` hoặc TypeSafe API key.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate-package.py
npx --yes skills@1.5.20 add . --list
claude plugin validate .
./scripts/package-skill.sh
python3 scripts/package-plugin.py
```

Skill packager cần `zip` và `unzip`; plugin packager dựng tiếp một ZIP chung cho hai nền tảng.
Các archive nằm trong `dist/`. Mỗi archive phải có `LICENSE`,
đúng public inventory và nội dung khớp source.

Trước khi dựng lại, sao lưu archive hiện có cùng SHA-256 vào một thư mục local mới trong
`output/`; giữ nguyên asset đã phát hành. README, `docs/`, `CONTRIBUTING.md` và `AGENTS.md`
không thuộc payload hiện tại, nên chỉ sửa những file đó không cần dựng lại archive. Nếu sửa
file được đóng gói, dùng quy trình trên rồi đối chiếu inventory, CRC, version và bytes với source.
Đóng gói thành công không chứng minh quyền gửi hoặc Directory approval. Trạng thái intake OpenAI
và điều kiện tiếp tục nằm trong [báo cáo ngày 23/10/2026](docs/openai-marketplace-assessment-2026-10-23.md).

Từ v0.10.5, runner bổ sung `python3 -B -m jev prepare --input input.json` chạy offline, input v2 và
coverage theo câu/pattern/recipe. Bộ ca tổng hợp ở `tests/fixtures/segmentation/` cần gán nhãn độc lập
với scanner; không dùng corpus tự sinh từ output để chứng minh segmentation đúng. Các test context,
ledger, nhiều batch, fault và package đều chạy offline.

Runner Jev nằm trong `jev/`, chỉ dùng Python standard library và key do host inject.
Không lấy runtime từ nghiên cứu cũ hoặc thêm đường dẫn máy maintainer. Sau khi sửa recipe hoặc
pattern canonical, chạy `python3 -B scripts/build-jev-registry.py` rồi kiểm `--check`. Registry
được track và phải đồng bộ trong mọi archive. Chạy test runtime bằng
`python3 -B -m unittest tests.test_jev -v`; live smoke chỉ dùng dữ liệu giả lập được phép gửi,
không thay thế kiểm holdout cho policy số. Không gọi thật API trong test offline.

## Tooling Spec Kit cho maintainer

Repo giữ constitution, template, script, workflow và `specs/` để review quyết định phát triển.
Generated skills và integration state thuộc từng checkout, được `.gitignore` chặn.

Cài CLI từ tag đã dùng cho tooling hiện tại rồi tạo Codex integration trong clone:

```bash
uv tool install 'git+https://github.com/github/spec-kit.git@v1.0.5'
specify integration install codex --script sh --integration-options='--skills'
```

CLI sẽ tạo `.agents/skills/`, `.specify/init-options.json`, `.specify/integration.json` và
`.specify/integrations/codex.manifest.json`. Các file này không được commit. Script và template
chung đã có sẵn; thông báo giữ nguyên shared infrastructure khi bootstrap là hành vi mong đợi.
Không chạy `specify init --here --force` chỉ để cài integration vì lệnh đó còn refresh tooling chung.

Tooling được vendor từ GitHub Spec Kit v1.0.5 giữ [MIT notice của upstream](.specify/LICENSE).
[Source licence tại tag đó](https://github.com/github/spec-kit/blob/v1.0.5/LICENSE).

## File được chia sẻ và file local

- Giữ source, fixtures, corpus có provenance, policy/config đã duyệt, lockfile và evidence public
  trong Git. `specs/*/research.md` là tài liệu thiết kế; `specs/*/evidence/` chứa báo cáo đã duyệt.
- `artifacts/` dành cho raw evaluation runs; `output/` và root `research/` dành cho scratch output.
  Các thư mục này, `dist/`, agent local state, cache và environment files được ignore.
- `.agents/skills/` là tooling sinh local; `.agents/plugins/marketplace.json` là catalog phân phối
  phải được track. Không ignore toàn bộ `.agents/` khi thêm integration mới.
- `.env.example` và `.env.*.example` được phép commit khi chỉ chứa placeholder.
- Corpus holdout đã được quan sát là evidence lịch sử. Trạng thái workflow `sealed` không làm file
  public trở thành bí mật; đánh giá độc lập tương lai phải dùng tập mới với quyền truy cập phù hợp.

## Trước khi gửi pull request

Giữ diff trong phạm vi thay đổi, kèm lệnh kiểm tra và kết quả mới. Khi sửa rule, ghi bằng chứng
vào `calibration/LOG.md` trước và thêm ca chống sửa quá tay. Khi đổi cây file, cập nhật README và
AGENTS trong cùng diff. Thay đổi package phải giữ manifest, version và archive validation đồng bộ.

CI kiểm offline tests, package validation và tracked paths. `.gitignore` chỉ giảm khả năng commit
nhầm; nó không chặn `git add -f` và không thay thế review dữ liệu hoặc secret scanning.

## Tài liệu và hình benchmark

`README.md` là trang giới thiệu ngắn. Danh mục pattern đầy đủ nằm trong `docs/patterns.md`,
style card được giới thiệu trong `docs/style-and-voice.md`, nguồn trong `docs/sources.md` và
lịch sử đầy đủ trong `docs/changelog.md`. Khi đổi version, cập nhật cả tóm tắt README và changelog.
Validator kiểm cả các tài liệu này; chuyển bảng không được làm mất kiểm tra inventory.

Hình README dùng lại dữ liệu trong báo cáo đã đóng băng, không chạy model. Xem
[hướng dẫn tái dựng hình](docs/figures/README.md). Bộ vẽ là tooling tùy chọn cho maintainer,
không thuộc payload hoặc dependency của người cài skill. Không dựng lại hay thay archive
đã phát hành chỉ vì sửa tài liệu ngoài payload.
