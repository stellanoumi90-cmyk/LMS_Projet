from django.db import models
from django.contrib.auth.models import User

# 1. RÔLES DES UTILISATEURS
class Profile(models.Model):
    ROLE_CHOICES = [
        ('promoteur', 'Promoteur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# 2. MODÈLE DE COURS (Ton modèle d'origine complété)
class course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    enseignant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'profile__role': 'enseignant'}, related_name='cours_enseignes')

    def __str__(self):
        return f"{self.code} - {self.name}"


# 3. LEÇONS (Avec support PDF ou Vidéo)
class Lecon(models.Model):
    cours = models.ForeignKey(course, on_delete=models.CASCADE, related_name='lecons')
    titre = models.CharField(max_length=200)
    document_pdf = models.FileField(upload_to='lecons_pdf/', blank=True, null=True)
    lien_video = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.cours.name} - {self.titre}"


# 4. ÉVALUATIONS PAR LEÇON
class Evaluation(models.Model):
    lecon = models.OneToOneField(Lecon, on_delete=models.CASCADE, related_name='evaluation')
    titre = models.CharField(max_length=200)
    note_maximale = models.IntegerField(default=20)

    def __str__(self):
        return f"Évaluation : {self.lecon.titre}"


# 5. NOTES ET PROGRESSION DE L'ÉTUDIANT
class NoteEtudiant(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'etudiant'})
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    note_obtenue = models.FloatField()
    date_passage = models.DateTimeField(auto_now_add=True)

    def pourcentage_reussite(self):
        # Calcule automatiquement le pourcentage obtenu à l'évaluation
        return (self.note_obtenue / self.evaluation.note_maximale) * 100

    def __str__(self):
        return f"{self.etudiant.username} - {self.evaluation.lecon.titre} : {self.note_obtenue}/{self.evaluation.note_maximale}"
        
class Certificat(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'etudiant'})
    cours = models.ForeignKey(course, on_delete=models.CASCADE)
    date_delivrance = models.DateTimeField(auto_now_add=True)
    code_verification = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Génère un code de vérification unique pour le certificat avant de sauvegarder
        if not self.code_verification:
            import uuid
            self.code_verification = f"CERT-{self.cours.code}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

@receiver(post_save, sender=NoteEtudiant) 
def generer_certificat_automatique(sender, instance, created, **kwargs):
    # On vérifie si la note saisie est supérieure ou égale à la moyenne (ex: 10/20)
    # Adapte 'instance.note' avec le nom exact de ton champ de note
    if instance.note >= 10: 
        # On vérifie si le certificat n'existe pas déjà pour éviter les doublons
        certificat_existe = Certificat.objects.filter(
            etudiant=instance.etudiant, 
            cours=instance.cours
        ).exists()
        
        if not certificat_existe:
            # Création automatique du certificat lié
            Certificat.objects.create(
                etudiant=instance.etudiant,
                cours=instance.cours,
                code_verification=str(uuid.uuid4())[:8].upper() # Génère un code unique court
            )        

    def __str__(self):
        return f"Certificat {self.cours.name} - {self.etudiant.username}"        
