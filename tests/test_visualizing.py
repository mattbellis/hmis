import hmis
import folium


filename = 'test_data/hmis_test_data.pkl'
master_dictionary = hmis.read_dictionary_file(filename)

def test_get_plotting_style():
    ptype = 'Emergency Shelter'
    
    color,width,alpha,style = hmis.get_plotting_style(ptype)
    
    assert color == 'rgba(152, 150, 0, .8)'
    assert width == 2
    assert style == '-'
    assert alpha == 1.0
    
    
    
def test_plot_program_locations():
    
    map1 = hmis.plot_program_locations(master_dictionary)
    assert isinstance(map1, folium.Map)
