###
### init.pp: install sklearn, with all necessary dependencies.
###

class sklearn {
    ## create '/vagrant/build/' directory
    contain system::build_directory

    ## install sklearn dependencies
    contain package::sklearn_dependencies

    ## download scikit-learn
    contain package::sklearn

    ## build scikit-learn
    contain sklearn::build_sklearn

    ## install scikit-learn
    contain sklearn::install_sklearn
}
contain sklearn