# django imports
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
# tastypie imports
from tastypie.api import Api
# django imports
from api import DistrictResource, LanguageResource, MediatorResource, NonNegotiableResource, PartnerResource, PersonAdoptVideoResource, PersonGroupResource, PersonResource, ScreeningResource, VideoResource, VillageResource, CategoryResource, SubCategoryResource, VideoPracticeResource, DirectBeneficiariesResource, ParentCategoryResource, FrontLineWorkerPresentResource
from views import coco_v2, debug, login, logout, record_full_download_time, reset_database_check, upload_data

from dg.base_settings import COCO_PAGE
from dg.coco_admin import coco_admin

import output.urls
import raw_data_analytics.urls

v1_api = Api(api_name='v2')
v1_api.register(DistrictResource())
v1_api.register(LanguageResource())
v1_api.register(PartnerResource())
v1_api.register(VillageResource())
v1_api.register(MediatorResource())
v1_api.register(PersonAdoptVideoResource())
v1_api.register(PersonResource())
v1_api.register(PersonGroupResource())
v1_api.register(ScreeningResource())
v1_api.register(VideoResource())
v1_api.register(NonNegotiableResource())
v1_api.register(CategoryResource())
v1_api.register(SubCategoryResource())
v1_api.register(VideoPracticeResource())
v1_api.register(ParentCategoryResource())
v1_api.register(DirectBeneficiariesResource())
v1_api.register(FrontLineWorkerPresentResource())

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=COCO_PAGE)),
    (r'^api/', include(v1_api.urls)),
    (r'^login/', login),
    (r'^logout/', logout),
    (r'^debug/', debug),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name="faq"),
    (r'^record_full_download_time/', record_full_download_time),
    (r'^reset_database_check/', reset_database_check),
    (r'^upload/data/', upload_data),
    (r'^admin/coco/cocouser/add/state_wise_district', 'coco.admin_views.state_wise_district'),
    (r'^admin/coco/cocouser/add/district_wise_village', 'coco.admin_views.district_wise_village'),
    (r'^admin/coco/cocouser/add/partner_wise_video', 'coco.admin_views.partner_wise_video'),
    (r'^admin/coco/cocouser/add', 'coco.admin_views.add_cocouser'),
    (r'^admin/coco/cocouser/[0-9]', 'coco.admin_views.add_cocouser'),
    url(r'^admin/', include(coco_admin.urls)),
    (r'coco/', coco_v2),
    (r'^analytics/', include(output.urls)),
    (r'^rda/', include(raw_data_analytics.urls)),
)
