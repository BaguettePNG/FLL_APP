from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.secret_key = 'ton_secret_key'  # Nécessaire pour utiliser flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'equipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lettres = db.Column(db.String(10), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    nb_joueurs = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Equipe {self.nom}>'

class JeuxDuRobot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    
    note_prof1 = db.Column(db.Float, nullable=False)
    score1 = db.Column(db.Float, nullable=False)
    note_prof2 = db.Column(db.Float, nullable=False)
    score2 = db.Column(db.Float, nullable=False)
    note_prof3 = db.Column(db.Float, nullable=False)
    score3 = db.Column(db.Float, nullable=False)
    
    equipe = db.relationship('Equipe', backref=db.backref('jeux_du_robot', lazy=True))

    def __repr__(self):
        return f'<JeuxDuRobot Equipe={self.equipe.nom} Scores=({self.score1}, {self.score2}, {self.score3})>'

class ConceptionRobot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)

    identify_Strategy = db.Column(db.Float, nullable=False)
    identify_research = db.Column(db.Float, nullable=False)
    design_ideas = db.Column(db.Float, nullable=False)
    design_building = db.Column(db.Float, nullable=False)
    create_attach = db.Column(db.Float, nullable=False)
    create_code = db.Column(db.Float, nullable=False)
    iterate_testing = db.Column(db.Float, nullable=False)
    iterate_improv = db.Column(db.Float, nullable=False)
    communication_impact = db.Column(db.Float, nullable=False)
    communication_fun = db.Column(db.Float, nullable=False)

    equipe = db.relationship('Equipe', backref=db.backref('conception_robot', lazy=True))

    def __repr__(self):
        return f'<ConceptionRobot Equipe={self.equipe.nom}>'

class Innovation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)

    identify_define = db.Column(db.Float, nullable=False)
    identify_research = db.Column(db.Float, nullable=False)
    design_plan = db.Column(db.Float, nullable=False)
    design_Teamworks = db.Column(db.Float, nullable=False)
    create_innovation = db.Column(db.Float, nullable=False)
    create_model = db.Column(db.Float, nullable=False)
    iterate_sharing = db.Column(db.Float, nullable=False)
    iterate_improv = db.Column(db.Float, nullable=False)
    communication_impact = db.Column(db.Float, nullable=False)
    communication_fun = db.Column(db.Float, nullable=False)

    equipe = db.relationship('Equipe', backref=db.backref('Innovation', lazy=True))

    def __repr__(self):
        return f'<Innovation Equipe={self.equipe.nom}>'
    

class CoreValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)

    discovery_ip = db.Column(db.Float, nullable=False)
    Teamworks_ip = db.Column(db.Float, nullable=False)
    innovation_ip = db.Column(db.Float, nullable=False)
    impact_ip = db.Column(db.Float, nullable=False)
    fun_ip = db.Column(db.Float, nullable=False)
    discovery_rd = db.Column(db.Float, nullable=False)
    inclusion_rd = db.Column(db.Float, nullable=False)
    innovation_rd = db.Column(db.Float, nullable=False)
    impact_rd = db.Column(db.Float, nullable=False)
    fun_rd = db.Column(db.Float, nullable=False)

    equipe = db.relationship('Equipe', backref=db.backref('CoreValue', lazy=True))

    def __repr__(self):
        return f'<CoreValue Equipe={self.equipe.nom}>'

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/team", methods=["GET", "POST"])
def team():
    if request.method == "POST":
        try:
            nb_joueurs = int(request.form["nb_joueurs"])
            if nb_joueurs < 1:
                flash("Le nombre de joueurs doit être au moins 1.", "warning")
                return redirect(url_for("team"))
        except ValueError:
            flash("Le nombre de joueurs doit être un nombre entier.", "warning")
            return redirect(url_for("team"))

        equipe = Equipe(
            lettres=request.form["lettres"],
            nom=request.form["nom"],
            ville=request.form["ville"],
            nb_joueurs=nb_joueurs
        )
        db.session.add(equipe)
        db.session.commit()
        flash("Équipe ajoutée avec succès !", "success")
        return redirect(url_for("team"))

    equipes = Equipe.query.all()
    return render_template("team.html", equipes=equipes)

@app.route("/delete/<int:id>")
def delete_team(id):
    equipe = Equipe.query.get_or_404(id)
    db.session.delete(equipe)
    db.session.commit()
    flash("Équipe supprimée.", "info")
    return redirect(url_for("team"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_team(id):
    equipe = Equipe.query.get_or_404(id)
    if request.method == "POST":
        try:
            nb_joueurs = int(request.form["nb_joueurs"])
            if nb_joueurs < 1:
                flash("Le nombre de joueurs doit être au moins 1.", "warning")
                return redirect(url_for("edit_team", id=id))
        except ValueError:
            flash("Le nombre de joueurs doit être un nombre entier.", "warning")
            return redirect(url_for("edit_team", id=id))

        equipe.lettres = request.form["lettres"]
        equipe.nom = request.form["nom"]
        equipe.ville = request.form["ville"]
        equipe.nb_joueurs = nb_joueurs
        db.session.commit()
        flash("Équipe modifiée avec succès !", "success")
        return redirect(url_for("team"))

    return render_template("edit_team.html", equipe=equipe)

@app.route("/jeux_robot", methods=["GET", "POST"])
def jeux_robot():
    equipes = Equipe.query.all()
    if request.method == "POST":
        equipe_id = int(request.form["equipe_id"])
        note_prof1 = float(request.form["note_prof1"])
        score1 = float(request.form["score1"])
        note_prof2 = float(request.form["note_prof2"])
        score2 = float(request.form["score2"])
        note_prof3 = float(request.form["note_prof3"])
        score3 = float(request.form["score3"])

        jeu = JeuxDuRobot(
            equipe_id=equipe_id,
            note_prof1=note_prof1, score1=score1,
            note_prof2=note_prof2, score2=score2,
            note_prof3=note_prof3, score3=score3
        )
        db.session.add(jeu)
        db.session.commit()
        flash("Jeu du robot ajouté pour l'équipe avec succès !", "success")
        return redirect(url_for("jeux_robot"))
    
    return render_template("Jeux_Robot_main.html", equipes=equipes)


@app.route("/Formulaire_CR", methods=["GET", "POST"])
def esprit_equipe():
    equipes = Equipe.query.all()
    evaluations_existantes = {}
    for e in ConceptionRobot.query.all():
        evaluations_existantes[e.equipe_id] = {
            "identify_Strategy": e.identify_Strategy,
            "identify_research": e.identify_research,
            "design_ideas": e.design_ideas,
            "design_building": e.design_building,
            "create_attach": e.create_attach,
            "create_code": e.create_code,
            "iterate_testing": e.iterate_testing,
            "iterate_improv": e.iterate_improv,
            "communication_impact": e.communication_impact,
            "communication_fun": e.communication_fun
        }

    if request.method == "POST":
        try:
            champs = [
                "identify_Strategy", "identify_research",
                "design_ideas", "design_building",
                "create_attach", "create_code",
                "iterate_testing", "iterate_improv",
                "communication_impact", "communication_fun"
            ]
            for equipe in equipes:
                equipe_id = equipe.id
                valeurs = {}
                for champ in champs:
                    key = f"{champ}_{equipe_id}"
                    val = float(request.form[key])
                    if val < 1 or val > 4:
                        flash(f"Le champ '{champ}' de l'équipe {equipe.nom} doit être entre 1 et 4.", "warning")
                        return redirect(url_for("esprit_equipe"))
                    valeurs[champ] = val

                existing = ConceptionRobot.query.filter_by(equipe_id=equipe_id).first()
                if existing:
                    for champ, val in valeurs.items():
                        setattr(existing, champ, val)
                else:
                    esprit = ConceptionRobot(equipe_id=equipe_id, **valeurs)
                    db.session.add(esprit)

            db.session.commit()
            flash("Scores enregistrés avec succès !", "success")
            return redirect(url_for("esprit_equipe"))
        except Exception as e:
            flash(f"Erreur : {e}", "danger")
            return redirect(url_for("esprit_equipe"))

    return render_template("Formulaire_CR.html", equipes=equipes, evaluations=evaluations_existantes)

@app.route("/Scores_Jury")
def classement():
    # Conception du Robot
    classement_conception = []
    for e in ConceptionRobot.query.all():
        total = (
            e.identify_Strategy + e.identify_research +
            e.design_ideas + e.design_building +
            e.create_attach + e.create_code +
            e.iterate_testing + e.iterate_improv +
            e.communication_impact + e.communication_fun
        )
        classement_conception.append((e.equipe.nom, total))
    classement_conception.sort(key=lambda x: x[1], reverse=True)

    # Projet Innovation
    classement_innovation = []
    for e in Innovation.query.all():
        total = (
            e.identify_define + e.identify_research +
            e.design_plan + e.design_Teamworks +
            e.create_innovation + e.create_model +
            e.iterate_sharing + e.iterate_improv +
            e.communication_impact + e.communication_fun
        )
        classement_innovation.append((e.equipe.nom, total))
    classement_innovation.sort(key=lambda x: x[1], reverse=True)

    # Core Values
    classement_core_values = []
    for cv in CoreValue.query.all():
        total = (
            cv.discovery_ip + cv.Teamworks_ip + cv.innovation_ip +
            cv.impact_ip + cv.fun_ip +
            cv.discovery_rd + cv.inclusion_rd +
            cv.innovation_rd + cv.impact_rd + cv.fun_rd
        )
        classement_core_values.append((cv.equipe.nom, total))
    classement_core_values.sort(key=lambda x: x[1], reverse=True)

    return render_template(
        "Scores_Jury.html",
        classement_conception=classement_conception,
        classement_innovation=classement_innovation,
        classement_core_values=classement_core_values
    )

@app.route("/Formulaire_PI", methods=["GET", "POST"])
def formulaire_pi():
    equipes = Equipe.query.all()
    
    # Charger les évaluations existantes pour pré-remplir le formulaire
    evaluations_existantes = {}
    for e in Innovation.query.all():
        evaluations_existantes[e.equipe_id] = {
            "identify_define": e.identify_define,
            "identify_research": e.identify_research,
            "design_plan": e.design_plan,
            "design_Teamworks": e.design_Teamworks,
            "create_innovation": e.create_innovation,
            "create_model": e.create_model,
            "iterate_sharing": e.iterate_sharing,
            "iterate_improv": e.iterate_improv,
            "communication_impact": e.communication_impact,
            "communication_fun": e.communication_fun
        }
    
    if request.method == "POST":
        try:
            champs = [
                "identify_define", "identify_research",
                "design_plan", "design_Teamworks",
                "create_innovation", "create_model",
                "iterate_sharing", "iterate_improv",
                "communication_impact", "communication_fun"
            ]
            for equipe in equipes:
                equipe_id = equipe.id
                valeurs = {}
                for champ in champs:
                    key = f"{champ}_{equipe_id}"
                    val = float(request.form[key])
                    if val < 1 or val > 4:
                        flash(f"Le champ '{champ}' de l'équipe {equipe.nom} doit être entre 1 et 4.", "warning")
                        return redirect(url_for("formulaire_pi"))
                    valeurs[champ] = val
                
                existing = Innovation.query.filter_by(equipe_id=equipe_id).first()
                if existing:
                    for champ, val in valeurs.items():
                        setattr(existing, champ, val)
                else:
                    innovation = Innovation(equipe_id=equipe_id, **valeurs)
                    db.session.add(innovation)
            
            db.session.commit()
            flash("Scores du Projet Innovation enregistrés avec succès !", "success")
            return redirect(url_for("formulaire_pi"))
        except Exception as e:
            flash(f"Erreur : {e}", "danger")
            return redirect(url_for("formulaire_pi"))
    
    return render_template("Formulaire_PI.html", equipes=equipes, evaluations=evaluations_existantes)

@app.route("/Formulaire_EE", methods=["GET", "POST"])
def formulaire_ee():
    equipes = Equipe.query.all()

    evaluations_existantes = {
        e.equipe_id: {
            "discovery_ip": e.discovery_ip,
            "Teamworks_ip": e.Teamworks_ip,
            "innovation_ip": e.innovation_ip,
            "impact_ip": e.impact_ip,
            "fun_ip": e.fun_ip,
            "discovery_rd": e.discovery_rd,
            "inclusion_rd": e.inclusion_rd,
            "innovation_rd": e.innovation_rd,
            "impact_rd": e.impact_rd,
            "fun_rd": e.fun_rd,
        }
        for e in CoreValue.query.all()
    }

    if request.method == "POST":
        try:
            champs = [
                "discovery_ip", "Teamworks_ip", "innovation_ip", "impact_ip", "fun_ip",
                "discovery_rd", "inclusion_rd", "innovation_rd", "impact_rd", "fun_rd"
            ]
            for equipe in equipes:
                equipe_id = equipe.id
                valeurs = {}
                for champ in champs:
                    key = f"{champ}_{equipe_id}"
                    # Utilise get() pour éviter une KeyError si clé manquante
                    val_str = request.form.get(key)
                    if val_str is None:
                        flash(f"Le champ '{champ}' pour l'équipe {equipe.nom} est manquant.", "warning")
                        return redirect(url_for("formulaire_ee"))
                    try:
                        val = float(val_str)
                    except ValueError:
                        flash(f"Le champ '{champ}' pour l'équipe {equipe.nom} doit être un nombre.", "warning")
                        return redirect(url_for("formulaire_ee"))
                    if val < 1 or val > 4:
                        flash(f"Le champ '{champ}' pour l'équipe {equipe.nom} doit être entre 1 et 4.", "warning")
                        return redirect(url_for("formulaire_ee"))
                    valeurs[champ] = val

                existing = CoreValue.query.filter_by(equipe_id=equipe_id).first()
                if existing:
                    for champ, val in valeurs.items():
                        setattr(existing, champ, val)
                else:
                    cv = CoreValue(equipe_id=equipe_id, **valeurs)
                    db.session.add(cv)

            db.session.commit()
            flash("Scores des valeurs fondamentales enregistrés avec succès !", "success")
            return redirect(url_for("formulaire_ee"))
        except Exception as e:
            flash(f"Erreur inattendue : {e}", "danger")
            return redirect(url_for("formulaire_ee"))

    return render_template("Formulaire_EE.html", equipes=equipes, evaluations=evaluations_existantes)


@app.route("/score")
def score():
    # On récupère toutes les équipes avec leur(s) jeu(x) du robot
    equipes = Equipe.query.all()
    return render_template("score_robot.html", equipes=equipes)

@app.route("/affichage")
def affichage():
    equipes = Equipe.query.all()
    return render_template("affichage_public.html", equipes=equipes)

@app.route("/jury", methods=["GET", "POST"])
def jury_main():
    equipes = Equipe.query.all()    
    return render_template("jury_main.html", equipes=equipes)

@app.route("/parametres")
def parametres():
    return "Page Paramètres"

if __name__ == "__main__":
    app.run(debug=True)
