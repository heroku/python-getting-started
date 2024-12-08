# Python Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the tutorials for both the [Cedar and Fir generations](https://devcenter.heroku.com/articles/generations) of the Heroku platform. You can check them out here:

- [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Getting Started on Heroku Fir with Python](https://devcenter.heroku.com/articles/getting-started-with-python-fir)

## Deploying to Heroku

Using resources for this example app counts towards your usage. [Delete your app](https://devcenter.heroku.com/articles/heroku-cli-commands#heroku-apps-destroy) and [database](https://devcenter.heroku.com/articles/heroku-postgresql#removing-the-add-on) as soon as you are done experimenting to control costs.

### Deploy on Heroku [Cedar](https://devcenter.heroku.com/articles/generations#cedar)

By default, apps use Eco dynos if you are subscribed to Eco. Otherwise, it defaults to Basic dynos. The Eco dynos plan is shared across all Eco dynos in your account and is recommended if you plan on deploying many small apps to Heroku. Learn more about our low-cost plans [here](https://blog.heroku.com/new-low-cost-plans).

Eligible students can apply for platform credits through our new [Heroku for GitHub Students program](https://blog.heroku.com/github-student-developer-program).

```term
$ git clone https://github.com/heroku/python-getting-started
$ cd python-getting-started
$ heroku create
$ git push heroku main
$ heroku open
```

### Deploy on Heroku [Fir](https://devcenter.heroku.com/articles/generations#fir)

By default, apps on [Fir](https://devcenter.heroku.com/articles/generations#fir) use 1X-Classic dynos. To create an app on [Fir](https://devcenter.heroku.com/articles/generations#fir) you'll need to
[create a private space](https://devcenter.heroku.com/articles/working-with-private-spaces#create-a-private-space)
first.

```term
$ git clone https://github.com/heroku/python-getting-started
$ cd python-getting-started
$ heroku create --space <space-name>
$ git push heroku main
$ heroku ps:wait
$ heroku open
```

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
