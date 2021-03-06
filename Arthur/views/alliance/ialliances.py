# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009,2010 of Elliot Rosemarine.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
from sqlalchemy.orm import aliased
from sqlalchemy.sql import alias, asc, desc, case
from sqlalchemy.sql.functions import count, sum
from Core.config import Config
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu("Rankings", "Alliances (intel)", suffix="intel")
@load
class alliances(loadable):
    access = Config.get("Arthur", "intel")
    def execute(self, request, user, page="1", sort="score"):
        page = int(page)
        offset = (page - 1)*50
        order =  {"members" : (desc("ialliances_members"),),
                  "size"  : (desc("ialliances_size"),),
                  "value" : (desc("ialliances_value"),),
                  "score" : (desc("ialliances_score"),),
                  "avg_size"  : (desc("ialliances_avg_size"),),
                  "avg_value" : (desc("ialliances_avg_value"),),
                  "avg_score" : (desc("ialliances_avg_score"),),
                  "t10s"  : (desc("ialliances_t10s"),),
                  "t50s"  : (desc("ialliances_t50s"),),
                  "t100s" : (desc("ialliances_t100s"),),
                  "t200s" : (desc("ialliances_t200s"),),
                  "t10v"  : (desc("ialliances_t10v"),),
                  "t50v"  : (desc("ialliances_t50v"),),
                  "t100v" : (desc("ialliances_t100v"),),
                  "t200v" : (desc("ialliances_t200v"),),
                  } 
        if sort not in order.keys():
            sort = "score"
        order = order.get(sort)
        
        members = count().label("members")
        size = sum(Planet.size).label("size")
        value = sum(Planet.value).label("value")
        score = sum(Planet.score).label("score")
        avg_size = size.op("/")(members).label("avg_size")
        avg_value = value.op("/")(members).label("avg_value")
        avg_score = score.op("/")(members).label("avg_score")
        t10s = count(case(whens=((Planet.score_rank <= 10 ,1),), else_=None)).label("t10s")
        t50s = count(case(whens=((Planet.score_rank <= 50 ,1),), else_=None)).label("t50s")
        t100s = count(case(whens=((Planet.score_rank <= 100 ,1),), else_=None)).label("t100s")
        t200s = count(case(whens=((Planet.score_rank <= 200 ,1),), else_=None)).label("t200s")
        t10v = count(case(whens=((Planet.value_rank <= 10 ,1),), else_=None)).label("t10v")
        t50v = count(case(whens=((Planet.value_rank <= 50 ,1),), else_=None)).label("t50v")
        t100v = count(case(whens=((Planet.value_rank <= 100 ,1),), else_=None)).label("t100v")
        t200v = count(case(whens=((Planet.value_rank <= 200 ,1),), else_=None)).label("t200v")
        
        alliance1 = aliased(Alliance)
        Q = session.query(size, value, score,
                          avg_size, avg_value, avg_score,
                          t10s, t50s, t100s, t200s,
                          t10v, t50v, t100v, t200v,
                          members,
                          alliance1.id,
                          )
        Q = Q.join(Planet.intel)
        Q = Q.join((alliance1, Intel.alliance,))
        Q = Q.filter(Planet.active == True)
        Q = Q.group_by(alliance1.id)
        ialliances = alias(Q.subquery(), "ialliances")
        
        alliance2 = aliased(Alliance)
        Q = session.query(alliance2.name, alliance2.members)
        Q = Q.add_columns(ialliances)
        Q = Q.filter(alliance2.id == ialliances.c.id)
        
        count_ = Q.count()
        pages = count_/50 + int(count_%50 > 0)
        pages = range(1, 1+pages)
        
        for o in order:
            Q = Q.order_by(o)
        Q = Q.limit(50).offset(offset)
        return render("ialliances.tpl", request, alliances=Q.all(), offset=offset, pages=pages, page=page, sort=sort)
