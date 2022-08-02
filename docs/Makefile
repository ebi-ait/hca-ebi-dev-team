
.PHONY: check-ruby
check-ruby:
	@if ! hash ruby; then \
		echo -e "\nLooks like ruby is not installed. See readme for instructions.\n";\
		false;\
	fi

.PHONY: build
build: check-ruby
	bundle install

.PHONY: start
start:
	bundle exec jekyll serve -c _config_local.yml

.PHONY: clean
clean:
	rm -rf .jekyll-cache _site