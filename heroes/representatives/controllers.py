from flask import Blueprint, render_template, redirect, request

from google.appengine.ext import ndb
import logging
import pickle

from .models import Rep
from heroes.sports.models import Sport

rep_bp = Blueprint('rep', __name__)

# RENDERING #

# A REP PAGE.
@rep_bp.route('/<key>/')
def rep_view(key):
    rep_key = ndb.Key(urlsafe=key)
    rep = rep_key.get()

    #SORT stats
    if rep.stats:
        rep.stats.sort(key=sortRepStats)

    country = rep_key.parent().get()


    #BREADCRUMB
    # country
    country = rep_key.parent().get()
    # sport
    sport = country.key.parent().get()

    breadcrumb_list = [sport, country]
    title = rep.title
    #END BREADCRUMB

    return render_template('/admin/rep.html',
        breadcrumb = breadcrumb_list,
        object_title=title,
        rep_object=rep,
        country_object=country,
    )

def sortRepStats(stat):
    sortid = stat["sort"]
    return sortid

#NEW rep PAGE
@rep_bp.route('/new/<key>')
def new_rep(key):
    country_key = ndb.Key(urlsafe=key)
    country = country_key.get()

    #BREADCRUMB
    # country
    # sport
    sport = country.key.parent().get()

    breadcrumb_list = [sport, country]
    #END BREADCRUMB

    return render_template('/admin/rep.html',
        breadcrumb = breadcrumb_list,
        object_title='New rep',
        country_object=country,
    )



# HANDLERS #

# ADD rep
@rep_bp.route('/add/<parent_key>', methods=['POST'])
def add_entry(parent_key):
    country_key = ndb.Key(urlsafe=parent_key)
    country = country_key.get()

    if request.form['uid'] == "None" or request.form['uid'] == "":
        logging.info("ADD >>>>>>>>>>>>>> UID empty - SKIP")
        rep = Rep(firstname=request.form['firstname'], lastname=request.form['lastname'], parent=country_key)

    else:
        rep_check = Rep.query(Rep.uid == request.form['uid']).fetch(1)
        if rep_check:
            logging.info("ADD >>>>>>>>>>>>>> UID is a duplicate. DID NOT ADD UID")
            rep = Rep(firstname=request.form['firstname'], lastname=request.form['lastname'], parent=country_key)   
        else:
            logging.info("ADD >>>>>>>>>>>>>> UID unique - ADD TO REP")
            rep = Rep(firstname=request.form['firstname'], lastname=request.form['lastname'], uid=request.form['uid'], parent=country_key) 

    rep.put()

    return redirect('/admin/rep/{}'.format(rep.key.urlsafe()))


# UPDATE rep
@rep_bp.route('/update/<key>', methods=['POST'])
def update_entry(key):
    rep_key = ndb.Key(urlsafe=key)
    rep = rep_key.get()
    rep.firstname = request.form['firstname']
    rep.lastname = request.form['lastname']

    # UID
    if request.form['uid'] == "None":
        logging.info(">>>>>>>>>>>>>> UID empty - SKIP")
    else:
        if rep.uid != request.form['uid']:  #if its changed...
            logging.info(">>>>>>>>>>>>>> UID different...")
            rep_check = Rep.query(Rep.uid == request.form['uid']).fetch(1)
            if rep_check:
                logging.info(">>>>>>>>>>>>>> New UID a duplicate - DID NOT SAVE")
                # bounce back
                #TODO add error message
                return redirect('/admin/rep/{}'.format(rep.key.urlsafe()))

            else:
                #its changed and unique
                logging.info(">>>>>>>>>>>>>> UID unique - UPDATE AND SAVE")
                rep.uid = request.form['uid']

        else:
            logging.info(">>>>>>>>>>>>>> UID the same as before - DID NOT UPDATE UID BUT DID SAVE THE REST")


    rep.put()
    return redirect('/admin/rep/{}'.format(rep.key.urlsafe()))

# ADD rep STATS
@rep_bp.route('/addstat/<key>', methods=['POST'])
def add_stat(key):
    rep_key = ndb.Key(urlsafe=key)
    rep = rep_key.get()

    if rep.stats:
        statsList = rep.stats
    else:
        statsList = []

    try:
        stat = {"sort":int(request.form['statsort']),"label":request.form['statlabel'],"value":request.form['statvalue']}
        statsList.append(stat)

        rep.stats = statsList
        rep.put()
    except:
        logging.info("stat wrong format")
    
    return redirect('/admin/rep/{}'.format(rep.key.urlsafe()))



# REMOVE rep STATS
@rep_bp.route('/removestat/<key>/<stat_index>', methods=['GET'])
def remove_stat(key, stat_index):
    rep_key = ndb.Key(urlsafe=key)
    rep = rep_key.get()

    rep.stats.pop(int(stat_index)-1)

    rep.put()

    #DO STUFF


    return redirect('/admin/rep/{}'.format(rep.key.urlsafe()))


